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
