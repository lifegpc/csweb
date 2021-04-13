import web


def isIE():
    ua: str = web.ctx.env.get("HTTP_USER_AGENT")
    if ua is None:
        return False
    return ua.find("Trident") > -1


def ifIEHideContent():
    if isIE():
        return ' style="display: none;"'
