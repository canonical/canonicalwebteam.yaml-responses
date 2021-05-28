# Core
import os
import unittest

# Local
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)
from tests.fixtures.flask.app import (
    app_redirects,
    app_permanent_redirects,
    app_empty_redirects,
    app_empty_deleted,
    app_deleted,
    app_deleted_callback,
)


this_dir = os.path.dirname(os.path.realpath(__file__))


class TestFlaskRedirects(unittest.TestCase):
    def setUp(self):
        """
        Set up Flask app for testing
        """

        self.app_redirects = app_redirects.test_client()
        self.app_permanent_redirects = app_permanent_redirects.test_client()
        self.app_empty_redirects = app_empty_redirects.test_client()

    def test_missing_file(self):
        """
        When given a non-existent file path,
        prepare_redirects should not error
        """

        prepare_redirects(path="/tmp/non-existent-file.yaml")

    def test_not_found(self):
        """
        When Flask has redirects, check 404s still work
        """

        redirect_missing = self.app_redirects.get("/hello-missing")

        self.assertEqual(redirect_missing.status_code, 404)

    def test_not_found_empty_yaml(self):
        """
        When Flask is given an empty redirects file,
        check 404s still work
        """

        redirect_missing = self.app_empty_redirects.get("/hello-missing")

        self.assertEqual(redirect_missing.status_code, 404)

    def test_basic_redirect(self):
        """
        When Flask has redirects, check basic redirect works
        """

        redirect = self.app_redirects.get("/hello")

        self.assertEqual(redirect.status_code, 302)
        self.assertEqual(
            redirect.headers.get("Location"), "http://localhost/world"
        )

    def test_query_redirect(self):
        """
        When Flask has redirects, check redirect works with query string
        """

        redirect = self.app_redirects.get("/hello?name=world")
        redirect_query = self.app_redirects.get("/hello-query?name=world")

        self.assertEqual(redirect.status_code, 302)
        self.assertEqual(redirect_query.status_code, 302)
        self.assertEqual(
            redirect.headers.get("Location"),
            "http://localhost/world?name=world",
        )
        self.assertEqual(
            redirect_query.headers.get("Location"),
            "http://localhost/world?query=query&name=world",
        )

    def test_permanent_redirect(self):
        """
        When Flask has redirects, check permanent redirects work
        """

        redirect = self.app_permanent_redirects.get("/hello")

        self.assertEqual(redirect.status_code, 301)
        self.assertEqual(
            redirect.headers.get("Location"), "http://localhost/world"
        )

    def test_regex_redirect(self):
        """
        When Flask has redirects from redirects.yaml,
        check RegEx redirects work
        """

        robin_redirect = self.app_redirects.get("/example-robin")
        peter_redirect = self.app_redirects.get("/example-peter")

        self.assertEqual(robin_redirect.status_code, 302)
        self.assertEqual(
            robin_redirect.headers.get("Location"), "http://example.com/robin"
        )
        self.assertEqual(peter_redirect.status_code, 302)
        self.assertEqual(
            peter_redirect.headers.get("Location"), "http://example.com/peter"
        )

    def test_homepage_view(self):
        """
        When Flask has redirects from redirects.yaml
        check normal homepage view still works
        """

        homepage = self.app_redirects.get("/homepage")

        self.assertEqual(homepage.data, b"hello world")


class TestFlaskDeleted(unittest.TestCase):
    def setUp(self):
        """
        Set up Flask app for testing
        """

        self.app_deleted = app_deleted.test_client()
        self.app_deleted_callback = app_deleted_callback.test_client()
        self.app_empty_deleted = app_empty_deleted.test_client()

    def test_missing_file(self):
        """
        When given a non-existent file path,
        prepare_redirects should not error
        """

        prepare_deleted(path="/tmp/non-existent-file.yaml")

    def test_empty_file(self):
        """
        When given an empty file path,
        prepare_redirects should not error
        """

        prepare_deleted(path="{this_dir}/fixtures/empty.yaml")

    def test_not_found(self):
        """
        When Flask has deleteds, check 404s still work
        """

        deleted_missing = self.app_deleted.get("/deleted/missing")

        self.assertEqual(deleted_missing.status_code, 404)

    def test_not_found_empty_yaml(self):
        """
        When Flask is given an empty deleted file,
        check 404s still work
        """

        deleted_missing = self.app_empty_deleted.get("/deleted/missing")

        self.assertEqual(deleted_missing.status_code, 404)

    def test_basic_deleted(self):
        """
        When Flask has deleted paths from deleted.yaml
        check basic deleted page works
        """

        redirect = self.app_deleted.get("/deleted")

        self.assertEqual(redirect.status_code, 410)
        self.assertEqual(redirect.data, b"page deleted")

    def test_deleted_regex(self):
        """
        When Flask has deleted paths from deleted.yaml
        check deleted regex paths work
        """

        redirect = self.app_deleted.get("/deleted/nonsense/regex")

        self.assertEqual(redirect.status_code, 410)
        self.assertEqual(redirect.data, b"page deleted")

    def test_deleted_subpath_404(self):
        """
        When Flask has deleted paths from deleted.yaml
        check 404 sub-path still works
        """

        redirect = self.app_deleted.get("/deleted/missing")

        self.assertEqual(redirect.status_code, 404)

    def test_deleted_with_message(self):
        """
        Check deleted pages with extra context info
        """

        deleted = self.app_deleted.get("/deleted/with/message")

        self.assertEqual(deleted.status_code, 410)
        self.assertEqual(deleted.data, b"Gone, gone, gone")

    def test_deleted_callback(self):
        """
        Check deleted pages with a custom callback view function
        """

        deleted_callback = self.app_deleted_callback.get("/deleted")

        self.assertEqual(deleted_callback.status_code, 410)
        self.assertEqual(deleted_callback.data, b"custom callback")


if __name__ == "__main__":
    unittest.main()
