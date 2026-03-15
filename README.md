# k8s-pdb-audit-cli

Small CLI to find multi-replica Kubernetes Deployments that either have no `PodDisruptionBudget` or have a drain-blocking PDB (`minAvailable >= replicas` or `maxUnavailable == 0`).
