from hashlib import sha256 as __sha256, md5 as __md5, sha512 as __sha512


def sha256(s, encoding='utf8') -> str:
    if isinstance(s, str):
        b = s.encode(encoding)
    elif isinstance(s, bytes):
        b = s
    else:
        b = str(s).encode(encoding)
    h = __sha256()
    h.update(b)
    return h.hexdigest()


def md5(s, encoding='utf8') -> str:
    if isinstance(s, str):
        b = s.encode(encoding)
    elif isinstance(s, bytes):
        b = s
    else:
        b = str(s).encode(encoding)
    h = __md5()
    h.update(b)
    return h.hexdigest()


def sha512(s, encoding='utf8') -> str:
    if isinstance(s, str):
        b = s.encode(encoding)
    elif isinstance(s, bytes):
        b = s
    else:
        b = str(s).encode(encoding)
    h = __sha512()
    h.update(b)
    return h.hexdigest()
