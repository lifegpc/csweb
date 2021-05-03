import web


def setCacheControl(time: int, private: bool = False):
    web.header("Cache-Control",
               f"{'private' if private else 'public'}, max-age={time}")


def sendCacheInfo(time: int, startTime: int, private: bool = False):
    setCacheControl(time, private)
    from time import strftime, gmtime, time_ns
    from constants import GMT_FORMAT
    web.header("Date", strftime(GMT_FORMAT, gmtime()))
    web.header("Age", round((time_ns() - startTime) / 1E9))
