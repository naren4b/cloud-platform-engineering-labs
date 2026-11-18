#!/usr/bin/env bash
# Inspect a pinned Nexus Helm chart. Does not install Nexus.
set -euo pipefail

CHART_VERSION="${CHART_VERSION:-98.1.0}"
CHART_REPO="https://sonatype.github.io/helm3-charts/"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

helm repo add sonatype "$CHART_REPO" --force-update >/dev/null
helm repo update sonatype >/dev/null
helm show chart sonatype/nxrm-ha --version "$CHART_VERSION"

helm pull sonatype/nxrm-ha --version "$CHART_VERSION" --destination "$WORK_DIR"
tar -xzf "$WORK_DIR/nxrm-ha-$CHART_VERSION.tgz" -C "$WORK_DIR"

echo "Nexus license and PostgreSQL settings:"
grep -RniE 'licenseFile|licenseSecret|jdbc|postgres|clustered' \
  "$WORK_DIR/nxrm-ha/templates" "$WORK_DIR/nxrm-ha/values.yaml" || true

echo "Review these settings before configuring Nexus CE."
