"""
Quick-and-dirty script to bootstrap functional tests
for Django views.

You give it an app name; it loads all that app's URL patterns and
generates a trivial stub integration test case for each pattern.
"""


package_skel = """\
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

"""

testclass_skel = """\
class Test%(app)s(TestCase):

    fixtures = []
"""

testmethod_skel = """\
    def %(testname)s(self):
        client = Client()
        url = reverse(%(urlname)r,
                      %(urlargs)s)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
"""


def main(app):
    from django.utils.importlib import import_module
    urls = import_module('.urls', app)
    print package_skel
    # Convert lower_with_underscores to CamelCase
    app_title = app.split('_')
    app_title = ''.join([part.title() for part in app_title])

    print testclass_skel % {'app': app_title}
    for pattern in urls.urlpatterns:
        captured_kwargs = pattern.regex.groupindex.keys()
        testcase_kwargs = {}
        testcase_args = []
        if captured_kwargs:
            # It uses named regex groups.
            for key in captured_kwargs:
                # How to ensure that values match the regex?
                # Can't. Leave that up to the user.
                testcase_kwargs[key] = 'test'
        else:
            # It uses un-named regex groups.
            testcase_args = ['test'] * pattern.regex.groups

        ## We could inspect the view callable, as per
        ## http://www.szotten.com/david/introspecting-django-urls-for-fun-and-profit.html
        ## ... but unfortunately with class-based views and decorators
        ## and so on, we typically have only a function that accepts arbitrary
        ## keyword args as the callback.
        # import inspect
        # argspec = inspect.getargspec(pattern.callback)
        # args = argspec.args
        # defaults = argspec.defaults
        if testcase_kwargs:
            urlargs = 'kwargs=%s' % testcase_kwargs
        else:
            urlargs = 'args=%s' % testcase_args
        print testmethod_skel % {'testname': 'test_' + pattern.name,
                                 'urlname': pattern.name,
                                 'urlargs': urlargs,
                                 }


if __name__ == '__main__':
    import sys
    app_name = sys.argv[1]
    main(app_name)
