class DebugList:
    def __bool__(self):
        return self._i >= len(self._tl)

    def __init__(self, fn: str):
        self._i = 0
        fn2 = 'tests/' + fn
        with open(fn2, 'r', encoding='UTF-8') as f:
            t = f.read()
        self._tl = t.splitlines(False)

    def next(self):
        if self._i >= len(self._tl):
            raise ValueError('No more output data.')
        t = self._tl[self._i].replace('\\n', '\n')
        self._i += 1
        return t


def debug(*args, dl: DebugList):
    print(*args)
    a = []
    for i in args:
        a.append(str(i))
    t = " ".join(a)
    n = dl.next()
    if t != n:
        raise ValueError(f'Unexcepted value.\nNeeded Value: {n}')
