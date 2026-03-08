def labels_match(selector: dict, labels: dict) -> bool:
    if not selector:
        return False
    return all(labels.get(k) == v for k, v in selector.items())


def is_blocking_pdb(min_available, max_unavailable, replicas: int) -> bool:
    if replicas <= 1:
        return False
    if min_available is not None and str(min_available).isdigit():
        return int(min_available) >= replicas
    if max_unavailable is not None and str(max_unavailable).isdigit():
        return int(max_unavailable) == 0
    return False
