import os
import unittest
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import zope.component.testing
import zope.configuration.xmlconfig

import zope.pagetemplate.pagetemplatefile
import z3c.pt

def benchmark(title):
    def decorator(f):
        def wrapper(*args):
            print "==========================\n %s\n==========================" % title
            return f(*args)
        return wrapper
    return decorator

def timing(func, *args, **kwargs):
    t1 = t2 = time.time()
    i = 0
    while t2 - t1 < 3:
        func(*args, **kwargs)
        i += 1
        t2 = time.time()
    return 100*(t2-t1)/i
           
class BenchmarkTestCase(unittest.TestCase):

    table = [dict(a=1,b=2,c=3,d=4,e=5,f=6,g=7,h=8,i=9,j=10) \
             for x in range(1000)]

    helloworld_z3c = z3c.pt.PageTemplate("""\
    <div xmlns="http://www.w3.org/1999/xhtml">
    Hello World!
    </div>""")

    helloworld_zope = zope.pagetemplate.pagetemplate.PageTemplate()
    helloworld_zope.pt_edit("""\
    <div xmlns="http://www.w3.org/1999/xhtml">
    Hello World!
    </div>""", 'text/xhtml')
    
    bigtable_python_z3c = z3c.pt.PageTemplate("""\
    <table xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
    <tr tal:repeat="row table">
    <td tal:repeat="c row.values()">
    <span tal:define="d c + 1"
    tal:attributes="class 'column-' + str(d)"
    tal:content="d" />
    </td>
    </tr>
    </table>""")

    bigtable_path_z3c = z3c.pt.PageTemplate("""\
    <table xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    tal:default-expression="path">
    <tr tal:repeat="row table">
    <td tal:repeat="c row/values">
    <span tal:define="d python: c + 1"
    tal:attributes="class string:column-${d}"
    tal:content="d" />
    </td>
    </tr>
    </table>""")

    bigtable_i18n_z3c = z3c.pt.PageTemplate("""\
    <table xmlns="http://www.w3.org/1999/xhtml"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    i18n:domain="domain">
    <tr tal:repeat="row table">
    <span i18n:translate="label_default">Default</span>
    <td tal:repeat="c row.values()">
    <span tal:define="d c + 1"
    tal:attributes="class 'column-' + str(d)"
    tal:content="d" i18n:attributes="class" />
    <span i18n:translate="">Default</span>
    </td>
    </tr>
    </table>""")

    bigtable_python_zope = zope.pagetemplate.pagetemplate.PageTemplate()
    bigtable_python_zope.pt_edit("""\
    <table xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
    <tr tal:repeat="row python: options['table']">
    <td tal:repeat="c python: row.values()">
    <span tal:define="d python: c + 1"
    tal:attributes="class python:'column-'+str(d)"
    tal:content="d" />
    </td>
    </tr>
    </table>""", 'text/xhtml')

    bigtable_path_zope = zope.pagetemplate.pagetemplate.PageTemplate()
    bigtable_path_zope.pt_edit("""\
    <table xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
    <tr tal:repeat="row options/table">
    <td tal:repeat="c row/values">
    <span tal:define="d python: c + 1"
    tal:attributes="class string:column-${d}"
    tal:content="d" />
    </td>
    </tr>
    </table>""", 'text/xhtml')

    bigtable_i18n_zope = zope.pagetemplate.pagetemplate.PageTemplate()
    bigtable_i18n_zope.pt_edit("""\
    <table xmlns="http://www.w3.org/1999/xhtml"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    i18n:domain="domain">
    <tr tal:repeat="row python: options['table']">
    <span i18n:translate="label_default">Default</span>
    <td tal:repeat="c python: row.values()">
    <span tal:define="d python: c + 1"
    tal:attributes="class python:'column-'+str(d)"
    tal:content="d" i18n:attributes="class" />
    <span i18n:translate="">Default</span>
    </td>
    </tr>
    </table>""", 'text/xhtml')

    def setUp(suite):
        zope.component.testing.setUp(suite)
        zope.configuration.xmlconfig.XMLConfig('configure.zcml', z3c.pt)()

    def tearDown(suite):
        zope.component.testing.tearDown(suite)

    @benchmark(u"Hello World")
    def testHelloWorld(self):
        t_z3c = timing(self.helloworld_z3c)
        t_zope = timing(self.helloworld_zope)

        print "z3c.pt:            %.2f" % t_z3c
        print "zope.pagetemplate: %.2f" % t_zope
        print "                   %.2fX" % (t_zope/t_z3c)

    @benchmark(u"Big table (python)")
    def testBigTablePython(self):
        table = self.table

        t_z3c = timing(self.bigtable_python_z3c, table=table)
        t_zope = timing(self.bigtable_python_zope, table=table)

        print "z3c.pt:            %.2f" % t_z3c
        print "zope.pagetemplate: %.2f" % t_zope
        print "                   %.2fX" % (t_zope/t_z3c)

    @benchmark(u"Big table (path)")
    def testBigTablePath(self):
        table = self.table

        t_z3c = timing(self.bigtable_path_z3c, table=table, request=object())
        t_zope = timing(self.bigtable_path_zope, table=table)

        print "z3c.pt:            %.2f" % t_z3c
        print "zope.pagetemplate: %.2f" % t_zope
        print "                   %.2fX" % (t_zope/t_z3c)

    @benchmark(u"Compilation")
    def testCompilation(self):
        table = self.table

        t_z3c = timing(self.bigtable_python_z3c.cook, ['table'])
        t_zope = timing(self.bigtable_python_zope._cook)

        print "z3c.pt:            %.2f" % t_z3c
        print "zope.pagetemplate: %.2f" % t_zope
        print "                   %.2fX" % (t_zope/t_z3c)

    @benchmark(u"Internationalization")
    def testI18N(self):
        table = self.table

        t_z3c = timing(self.bigtable_i18n_z3c, table=table)
        t_zope = timing(self.bigtable_i18n_zope, table=table)

        print "z3c.pt:            %.2f" % t_z3c
        print "zope.pagetemplate: %.2f" % t_zope
        print "                   %.2fX" % (t_zope/t_z3c)

def test_suite():
    return unittest.makeSuite(BenchmarkTestCase)

if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")

