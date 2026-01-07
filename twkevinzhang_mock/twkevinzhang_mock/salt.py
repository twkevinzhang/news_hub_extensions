def encode(s: str) -> str:
    if s is None:
        return None
    return 'mock_' + s

def decode(s: str) -> str:
    if s is None:
        return None
    if s.startswith('mock_'):
        return s[5:]
    return s
