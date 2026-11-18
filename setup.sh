#!/usr/bin/env bash
# Verify the existing KIND platform before application deployment.
# Read-only checks. No Kubernetes resources are changed.
set -euo pipefail

for command in kubectl helm kind; do
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
