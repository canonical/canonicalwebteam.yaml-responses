# Core
import os
import unittest

# Packages
import django
from django.conf import settings
from django.test import Client
from django.test.utils import override_settings

# Local
from canonicalwebteam.yaml_responses.django import (
    create_redirect_views,
    create_deleted_views,
)


this_dir = os.path.dirname(os.path.realpath(__file__))

# Mock Django
settings.configure(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [f"{this_dir}/fixtures/django/templates"],
        }
    ],
)
django.setup()


class TestDjangoRedirects(unittest.TestCase):
    def test_missing_file(self):
        """
        When given a non-existent file path,
        create_redirect_views should return an empty list
        """

        self.assertEqual(
            create_redirect_views(path="/tmp/non-existent-file.yaml"), []
        )

    @override_settings(ROOT_URLCONF="tests.fixtures.django.redirects_urls")
    def test_not_found(self):
        """
        When Django has redirects from create_redirect_views,
        check 404s still work
        """

        django_client = Client()

        redirect_missing = django_client.get("/hello-missing")

        self.assertEqual(redirect_missing.status_code, 404)

    @override_settings(ROOT_URLCONF="tests.fixtures.django.redirects_urls")
    def test_basic_redirect(self):
        """
        When create_redirect_views is given a valid redirects.yaml file,
        and the resulting views are parsed by Django,
        check Django successfully redirects
        """

        django_client = Client()

        redirect = django_client.get("/hello")

        self.assertEqual(redirect.status_code, 302)
        self.assertEqual(redirect.get("Location"), "/world")

    @override_settings(
        ROOT_URLCONF="tests.fixtures.django.permanent_redirects_urls"
    )
    def test_permanent_redirect(self):
        """
        Check we can customise the status code
        to return e.g. a 301 response, instead of 302
        """

        django_client = Client()

        redirect = django_client.get("/hello")

        self.assertEqual(redirect.status_code, 301)
        self.assertEqual(redirect.get("Location"), "/world")

    @override_settings(ROOT_URLCONF="tests.fixtures.django.redirects_urls")
    def test_regex_redirect(self):
        """
        When create_redirect_views is given a valid redirects.yaml file,
        and the resulting views are parsed by Django,
        check Django successfully redirects
        """

        django_client = Client()

        robin_redirect = django_client.get("/example-robin")
        peter_redirect = django_client.get("/example-peter")

        self.assertEqual(robin_redirect.status_code, 302)
        self.assertEqual(
            robin_redirect.get("Location"), "http://example.com/robin"
        )
        self.assertEqual(peter_redirect.status_code, 302)
        self.assertEqual(
            peter_redirect.get("Location"), "http://example.com/peter"
        )

    @override_settings(ROOT_URLCONF="tests.fixtures.django.redirects_urls")
    def test_homepage_view(self):
        """
        When redirects from create_redirect_views are successfully passed to
        Django, check other normal views still work.
        """

        django_client = Client()

        homepage = django_client.get("/homepage")

        self.assertEqual(homepage.content, b"hello world")


class TestDjangoDeleted(unittest.TestCase):
    def test_missing_file(self):
        """
        When given a non-existent file path,
        create_deleted_views should return an empty list
        """

        self.assertEqual(
            create_deleted_views(path="/tmp/non-existent-file.yaml"), []
        )

    @override_settings(ROOT_URLCONF="tests.fixtures.django.deleted_urls")
    def test_basic_deleted(self):
        """
        When create_deleted_views is given a valid deleted.yaml file,
        and the resulting views are parsed by Django,
        check Django successfully shows 410 deleted page
        """

        django_client = Client()

        redirect = django_client.get("/deleted")

        self.assertEqual(redirect.status_code, 410)
        self.assertEqual(redirect.content, b"page deleted")

    @override_settings(ROOT_URLCONF="tests.fixtures.django.deleted_urls")
    def test_deleted_regex(self):
        """
        When create_deleted_views is given a valid deleted.yaml file,
        and the resulting views are parsed by Django,
        check Django successfully shows 410 deleted page for a regex path
        """

        django_client = Client()

        redirect = django_client.get("/deleted/nonsense/regex")

        self.assertEqual(redirect.status_code, 410)
        self.assertEqual(redirect.content, b"page deleted")

    @override_settings(ROOT_URLCONF="tests.fixtures.django.deleted_urls")
    def test_deleted_subpath_404(self):
        """
        When create_deleted_views is given a valid deleted.yaml file,
        and the resulting views are parsed by Django,
        check Django still shows 404 for non-matches
        """

        django_client = Client()

        redirect = django_client.get("/deleted/missing")

        self.assertEqual(redirect.status_code, 404)

    @override_settings(ROOT_URLCONF="tests.fixtures.django.deleted_urls")
    def test_deleted_with_message(self):
        """
        Check deleted pages with extra context info
        """

        django_client = Client()

        redirect = django_client.get("/deleted/with/message")

        self.assertEqual(redirect.status_code, 410)
        self.assertEqual(redirect.content, b"Gone, gone, gone")

    @override_settings(
        ROOT_URLCONF="tests.fixtures.django.deleted_callback_urls"
    )
    def test_deleted_callback(self):
        """
        Check deleted pages with a custom callback view function
        """

        django_client = Client()

        redirect = django_client.get("/deleted")

        self.assertEqual(redirect.status_code, 410)
        self.assertEqual(redirect.content, b"custom callback")


if __name__ == "__main__":
    unittest.main()
