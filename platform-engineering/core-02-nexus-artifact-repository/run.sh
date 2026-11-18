#!/usr/bin/env bash
# Inspect the Nexus chart and check the existing KIND platform.
# This script does not install or modify Kubernetes resources.
set -euo pipefail

CHART_VERSION="${CHART_VERSION:-98.1.0}"
CHART_REPO="https://sonatype.github.io/helm3-charts/"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

for command in kubectl helm kind tar grep; do
  command -v "$command" >/dev/null || { echo "Missing: $command" >&2; exit 1; }
done

context="$(kubectl config current-context)"
case "$context" in
  kind-*) echo "Kubernetes context: $context" ;;
  *) echo "Expected a KIND context, got: $context" >&2; exit 1 ;;
esac

echo "Checking platform resources..."
kubectl get nodes
kubectl get storageclass
kubectl get gatewayclass
kubectl get gateways -A

echo "Fetching Sonatype chart $CHART_VERSION..."
helm repo add sonatype "$CHART_REPO" --force-update >/dev/null
helm repo update sonatype >/dev/null
helm show chart sonatype/nxrm-ha --version "$CHART_VERSION"

helm pull sonatype/nxrm-ha --version "$CHART_VERSION" --destination "$WORK_DIR"
tar -xzf "$WORK_DIR/nxrm-ha-$CHART_VERSION.tgz" -C "$WORK_DIR"

echo "Checking license and database settings..."
grep -RniE 'licenseFile|licenseSecret|jdbc|postgres|clustered' \
  "$WORK_DIR/nxrm-ha/templates" "$WORK_DIR/nxrm-ha/values.yaml" || true

echo
echo "Review the chart output before configuring or installing Nexus CE."
