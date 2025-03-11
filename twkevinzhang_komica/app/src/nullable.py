from google.protobuf.internal.containers import ScalarMap


def is_zero_str(s: str | None):
    return s is None or s == ""

def is_zero_int(i: int | None):
    return i is None or i == 0

def is_zero_list(l: list | None):
    return l is None or len(l) == 0

def is_zero_map(d: ScalarMap | None):
    return d is None or len(d.keys()) == 0
