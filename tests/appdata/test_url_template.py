import unittest

from sqldiff.appdata.url_template import MandatoryFieldsUrlTemplate, OptionalFieldsUrlTemplate, JdbcUrlTemplate


class TestMandatoryFieldsUrlTemplate(unittest.TestCase):

    def test_proper_fields(self):
        template = 'jdbc:postgresql://{host}:{port}'
        url_template = MandatoryFieldsUrlTemplate(template)
        args = {'host': 'test_host', 'port': 1234}
        url = url_template.feed(args)
        self.assertEqual(url, 'jdbc:postgresql://test_host:1234')

    def test_missing_fields(self):
        with self.assertRaises(KeyError) as context:
            template = 'jdbc:postgresql://{host}:{port}'
            url_template = MandatoryFieldsUrlTemplate(template)
            args = {'host': 'test_host'}
            url = url_template.feed(args)


class TestOptionalFieldsUrlTemplate(unittest.TestCase):

    def test_proper_fields(self):
        template = 'jdbc:postgresql://[{host}][:{port}]'
        url_template = OptionalFieldsUrlTemplate(template)
        args = {'host': 'test_host', 'port': 1234}
        url = url_template.feed(args)
        self.assertEqual(url, 'jdbc:postgresql://test_host:1234')

    def test_missing_mandatory_fields(self):
        """Test that when value is missing, it will remove everything from square brackets"""
        template = 'jdbc:postgresql://[{host}][:{port}]'
        url_template = OptionalFieldsUrlTemplate(template)
        args = {'host': 'test_host'}
        url = url_template.feed(args)
        self.assertEqual(url, 'jdbc:postgresql://test_host')


class TestJdbcUrlTemplate(unittest.TestCase):

    def test_proper_mandatory_fields_only(self):
        template = 'jdbc:postgresql://{host}:{port}/[db={database}]'
        url_template = JdbcUrlTemplate(template)
        args = {'host': 'test_host', 'port': 1234}
        url = url_template.feed(args)
        self.assertEqual(url, 'jdbc:postgresql://test_host:1234/')

    def test_all_proper_fields(self):
        template = 'jdbc:postgresql://{host}:{port}/[db={database}]'
        url_template = JdbcUrlTemplate(template)
        args = {'host': 'test_host', 'port': 1234, 'database': 'test_db'}
        url = url_template.feed(args)
        self.assertEqual(url, 'jdbc:postgresql://test_host:1234/db=test_db')



