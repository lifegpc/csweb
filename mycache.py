import web


def setCacheControl(time: int, private: bool = False):
    web.header("Cache-Control",
               f"{'private' if private else 'public'}, max-age={time}")
