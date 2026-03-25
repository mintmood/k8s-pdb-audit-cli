# k8s-pdb-audit-cli

Small CLI to find multi-replica Kubernetes Deployments and StatefulSets that either have no `PodDisruptionBudget` or have a drain-blocking PDB (`minAvailable >= replicas` or `maxUnavailable == 0`).

## Usage

```bash
pip install -r requirements.txt
python3 pdb_audit.py -n production
```
