from hashlib import sha256 as __sha256, md5 as __md5


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


def md5(s) -> str:
    if isinstance(s, str):
        b = s.encode()
    elif isinstance(s, bytes):
        b = s
    else:
        b = str(s).encode()
    h = __md5()
    h.update(b)
    return h.hexdigest()
