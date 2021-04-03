from hashlib import sha256 as __sha256


def sha256(s) -> str:
    if isinstance(s, str):
        b = s.encode()
    elif isinstance(s, bytes):
        b = s
    else:
        b = str(s).encode()
    h = __sha256()
    h.update(b)
    return h.hexdigest()
