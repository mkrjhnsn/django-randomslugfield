from django.db import models
from django.test import TestCase

from .fields import RandomSlugField


class TestModel(models.Model):
    slug = RandomSlugField(length=7)
    slug_lower = RandomSlugField(length=7, exclude_upper=True,
                                 exclude_digits=True)
    slug_upper = RandomSlugField(length=7, exclude_lower=True,
                                 exclude_digits=True)
    slug_digits = RandomSlugField(length=7, exclude_lower=True,
                                  exclude_upper=True)


class RandomSlugFieldTest(TestCase):
    def test_slug_length(self):
        m = TestModel.objects.create()
        self.assertEqual(len(m.slug), 7)
        self.assertTrue(m.slug.isalnum())

    def test_slug_is_lowercase(self):
        m = TestModel.objects.create()
        self.assertTrue(m.slug_lower.islower() and m.slug_lower.isalpha())

    def test_slug_is_uppercase(self):
        m = TestModel.objects.create()
        self.assertTrue(m.slug_upper.isupper() and m.slug_upper.isalpha())

    def test_slug_is_all_digits(self):
        m = TestModel.objects.create()
        self.assertTrue(m.slug_digits.isdigit())
