def extra_variant_count(filename: str) -> int:
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                count += 1

    return count
