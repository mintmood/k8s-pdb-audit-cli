#!/usr/bin/env python3
import argparse
from kubernetes import client, config


def labels_match(selector: dict, labels: dict) -> bool:
    if not selector:
        return False
    return all(labels.get(k) == v for k, v in selector.items())


def is_blocking_pdb(min_available, max_unavailable, replicas: int) -> bool:
    if replicas <= 1:
        return False
    if min_available is not None:
        s = str(min_available)
        if s == "100%":
            return True
        if s.isdigit():
            return int(s) >= replicas
    if max_unavailable is not None:
        s = str(max_unavailable)
        if s in ("0", "0%"):
            return True
    return False


def main():
    p = argparse.ArgumentParser(description="Audit Deployments and StatefulSets for missing or blocking PDBs")
    p.add_argument("-n", "--namespace", default="")
    args = p.parse_args()
    config.load_kube_config()
    apps = client.AppsV1Api()
    policy = client.PolicyV1Api()
    deps = apps.list_namespaced_deployment(args.namespace).items if args.namespace else apps.list_deployment_for_all_namespaces().items
    stss = apps.list_namespaced_stateful_set(args.namespace).items if args.namespace else apps.list_stateful_set_for_all_namespaces().items
    pdbs = policy.list_namespaced_pod_disruption_budget(args.namespace).items if args.namespace else policy.list_pod_disruption_budget_for_all_namespaces().items
    for w in [*deps, *stss]:
        replicas = w.spec.replicas or 0
        if replicas < 2:
            continue
        pod_labels = w.spec.template.metadata.labels or {}
        matched = [b for b in pdbs if b.metadata.namespace == w.metadata.namespace and labels_match((b.spec.selector.match_labels or {}), pod_labels)]
        if not matched:
            print(f"{w.metadata.namespace}/{w.metadata.name}\tMISSING_PDB\treplicas={replicas}")
        else:
            for b in matched:
                if is_blocking_pdb(b.spec.min_available, b.spec.max_unavailable, replicas):
                    print(f"{w.metadata.namespace}/{w.metadata.name}\tBLOCKING_PDB\tpdb={b.metadata.name}")


if __name__ == "__main__":
    main()
