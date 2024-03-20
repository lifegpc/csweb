import geoip2.database
import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath("."))
    m = True
else:
    m = False
import web
from settings import settings
from traceback import format_exc


class Geoip:
    def GET(self, type, code):
        s = settings()
        s.ReadSettings()
        if not s.geoDatabase:
            return 'Geoip database not found'
        try:
            with geoip2.database.Reader(s.geoDatabase) as reader:
                if type == 'code':
                    response = reader.country(code)
                    return response.country.iso_code.lower()
                else:
                    web.HTTPError("400 Bad Request")
                    return 'Invalid type'
        except Exception:
            t = ''
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    t = format_exc()
            except:
                pass
            web.HTTPError('500 Internal Server Error')
            return t


if m:
    application = web.application(('(.*)/(.*)', 'Geoip'), globals()).wsgifunc()
