#!/usr/bin/env bash
# Nexus CE: inspect, render, deploy or check the pinned Sonatype chart.
# Use ./setup.sh at the repository root for shared KIND checks.
set -euo pipefail

ACTION="${1:-inspect}"
CHART_VERSION="${CHART_VERSION:-98.1.0}"
NAMESPACE="${NAMESPACE:-nexus}"
RELEASE="${RELEASE:-nexus}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

case "$ACTION" in
  inspect|render|deploy|status) ;;
  *) echo "Usage: $0 {inspect|render|deploy|status}" >&2; exit 2 ;;
esac

if [[ "$ACTION" == "status" ]]; then
  helm status "$RELEASE" -n "$NAMESPACE"
  kubectl get pods,svc,pvc -n "$NAMESPACE"
  exit
fi

for command in helm tar grep sed kubectl; do
  command -v "$command" >/dev/null || { echo "Missing: $command" >&2; exit 1; }
done

helm pull nxrm-ha --repo https://sonatype.github.io/helm3-charts/ \
  --version "$CHART_VERSION" --destination "$WORK_DIR"
tar -xzf "$WORK_DIR/nxrm-ha-$CHART_VERSION.tgz" -C "$WORK_DIR"
CHART="$WORK_DIR/nxrm-ha"
TEMPLATE="$CHART/templates/statefulset.yaml"

# The official chart adds a Pro license flag in both JVM modes.
count="$(grep -c -- '-Dnexus.licenseFile=\${LICENSE_FILE}' "$TEMPLATE" || true)"
if [[ "$count" != "2" ]]; then
  echo "Unexpected chart license template. Review version $CHART_VERSION." >&2
  exit 1
fi
sed -i 's/ -Dnexus\.licenseFile=\${LICENSE_FILE}//g' "$TEMPLATE"
if grep -q -- '-Dnexus.licenseFile' "$TEMPLATE"; then
  echo "CE license patch failed." >&2
  exit 1
fi

if [[ "$ACTION" == "inspect" ]]; then
  echo "Pinned chart: $CHART_VERSION"
  echo "CE adaptation: removed two Pro license JVM flags"
  grep -nE 'jdbc:postgresql|datastore.enabled|volumeClaimTemplates' "$TEMPLATE"
  exit
fi

helm lint "$CHART" -f "$DIR/values.yaml"
helm template "$RELEASE" "$CHART" -n "$NAMESPACE" \
  -f "$DIR/values.yaml" > "$WORK_DIR/rendered.yaml"
echo "Rendered patched Nexus chart: $CHART_VERSION"

if [[ "$ACTION" == "render" ]]; then
  echo "No cluster changes made."
  exit
fi

# Never install without an existing database and credentials.
kubectl get namespace "$NAMESPACE" >/dev/null
kubectl get secret nexus-db -n "$NAMESPACE" >/dev/null
kubectl get secret nxrm-ha-adminsecret -n "$NAMESPACE" >/dev/null
echo "Confirm the PostgreSQL Helm release is running and reachable."
read -r -p "Install Nexus in namespace $NAMESPACE? Type 'yes': " confirm
[[ "$confirm" == "yes" ]] || { echo "Cancelled."; exit 1; }

helm upgrade --install "$RELEASE" "$CHART" -n "$NAMESPACE" \
  -f "$DIR/values.yaml"
echo "Check rollout using: $0 status"
