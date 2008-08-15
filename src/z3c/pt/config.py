import os

truevals = ('y', 'yes', 't', 'true', 'on', '1')

DEBUG_MODE_KEY = 'Z3C_PT_DEBUG'
DEBUG_MODE = os.environ.get(DEBUG_MODE_KEY, 'false')
DEBUG_MODE = DEBUG_MODE.lower() in truevals

PROD_MODE = not DEBUG_MODE

VALIDATION = DEBUG_MODE

DISABLE_I18N_KEY = 'Z3C_PT_DISABLE_I18N'
DISABLE_I18N = os.environ.get(DISABLE_I18N_KEY, 'false')
DISABLE_I18N = DISABLE_I18N.lower() in truevals

XHTML_NS = "http://www.w3.org/1999/xhtml"
TAL_NS = "http://xml.zope.org/namespaces/tal"
META_NS = "http://xml.zope.org/namespaces/meta"
METAL_NS = "http://xml.zope.org/namespaces/metal"
I18N_NS = "http://xml.zope.org/namespaces/i18n"
PY_NS = "http://genshi.edgewall.org"
NS_MAP = dict(py=PY_NS, tal=TAL_NS, metal=METAL_NS)
