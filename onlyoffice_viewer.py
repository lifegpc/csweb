import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath("."))
    m = True
else:
    m = False
from urllib.parse import urlparse, unquote_plus
from json import dumps
import web
from hashl import sha512
from settings import settings
try:
    from jwt import encode as jwtencode
    have_jwt = True
except ImportError:
    have_jwt = False
from constants import jsonsep
from tep import getTemplate


class OnlyOfficeViewer:
    def GET(self, *k, **kw):
        te = getTemplate("onlyoffice_viewer.html")
        if te is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        s = settings()
        s.ReadSettings()
        if s.onlyOfficeEndpoint is None:
            web.HTTPError('500 Internal Server Error')
            if s.debug:
                return 'onlyOfficeEndpoint is not set'
            else:
                return 'Internal Server Error'
        url = web.input().get("url")
        if url is None or url == '':
            url = web.input().get("u")
        if url is None or url == '':
            web.HTTPError('400 Bad Request')
            return 'URL not specified.'
        parsed_url = urlparse(url)
        origin = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if origin not in s.onlyOfficeAllowOrigins:
            web.HTTPError('403 Forbidden')
            return 'Forbidden'
        title = web.input().get("title")
        if title is None or title == '':
            title = web.input().get("t")
        if title is None or title == '':
            title = unquote_plus(parsed_url.path.split('/')[-1])
        if title is None or title == '':
            title = 'Unknown title'
        key = web.input().get("key")
        if key is None or key == '':
            key = web.input().get("k")
        if key is None or key == '':
            key = sha512(url)
        fileType = web.input().get("file_type")
        if fileType is None or fileType == '':
            fileType = parsed_url.path.split('/')[-1].split(".")[-1]
            if fileType == title:
                web.HTTPError('400 Bad Request')
                return 'Failed to determine file type.'
        documentType = web.input().get("document_type")
        if documentType is None or documentType == '':
            if fileType in ['doc', 'docm', 'docx', 'docxf', 'dot', 'dotm', 'dotx', 'epub', 'fodt', 'fb2', 'htm', 'html', 'mht', 'odt', 'oform', 'ott', 'oxps', 'pdf', 'rtf', 'txt', 'djvu', 'xml', 'xps']:  # noqa: E501
                documentType = 'word'
            elif fileType in ['csv', 'fods', 'ods', 'ots', 'xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltm', 'xltx']:  # noqa: E501
                documentType = 'cell'
            elif fileType in ['fodp', 'odp', 'otp', 'pot', 'potm', 'potx', 'pps', 'ppsm', 'ppt', 'pptm', 'pptx']:  # noqa: E501
                documentType = 'slide'
            else:
                web.HTTPError('400 Bad Request')
                return 'Failed to determine document type.'
        if documentType not in ['word', 'slide', 'cell']:
            web.HTTPError('400 Bad Request')
            return 'Invalid document type.'
        config = {'document': {'title': title, 'url': url, 'key': key, 'fileType': fileType}, 'documentType': documentType}  # noqa: E501
        type = web.input().get("type")
        if type is not None and type not in ['desktop', 'mobile', 'embedded']:
            web.HTTPError('400 Bad Request')
            return 'Invalid type.'
        config['type'] = type
        height = web.input().get("height")
        if height is not None and height != '':
            config['height'] = height
        width = web.input().get("width")
        if width is not None and width != '':
            config['width'] = width
        secret = s.onlyOfficeToken
        if secret is not None:
            if not have_jwt:
                web.HTTPError('500 Internal Server Error')
                if s.debug:
                    return 'PyJWT not installed.'
                else:
                    return 'Internal Server Error'
            config['token'] = jwtencode(config, s.onlyOfficeToken)
        sconfig = dumps(config, ensure_ascii=False, separators=jsonsep)
        return te(config, sconfig, s.onlyOfficeEndpoint)


if m:
    application = web.application(('(/.*)', 'OnlyOfficeViewer'), globals()).wsgifunc()  # noqa: E501
