from unittest import skipIf

import django
from django.core.exceptions import FieldError
from django.db import models
from django.test import TestCase

from .fields import RandomSlugField


# Using length=255 to increase chances of getting invalid character in
# generated slug.
class FullSlug(models.Model):
    slug = RandomSlugField(length=255)


class UppercaseSlug(models.Model):
    slug = RandomSlugField(length=255, exclude_lower=True, exclude_digits=True)


class LowercaseSlug(models.Model):
    slug = RandomSlugField(length=255, exclude_upper=True, exclude_digits=True)


class DigitsSlug(models.Model):
    slug = RandomSlugField(length=255, exclude_lower=True, exclude_upper=True)


class NoVowelSlug(models.Model):
    slug = RandomSlugField(length=255, exclude_vowels=True)


class MaxSlugs(models.Model):
    slug = RandomSlugField(length=1, exclude_lower=True, exclude_upper=True)


class RandomSlugTestCase(TestCase):

    def test_slug_length(self):
        """Test to make sure slug is correct length."""
        FullSlug.objects.create()
        obj = FullSlug.objects.get(pk=1)
        self.assertEqual(len(obj.slug), 255)

    def test_slug_charset(self):
        """Test to make sure slug only contains ascii characters and
        digits.
        """
        FullSlug.objects.create()
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                '0123456789'
        obj = FullSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isalnum())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_is_uppercase(self):
        """Test to make sure slug only contains uppercase characters."""
        UppercaseSlug.objects.create()
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        obj = UppercaseSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isupper() and obj.slug.isalpha())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_is_lowercase(self):
        """Test to make sure slug only contains lowercase characters."""
        LowercaseSlug.objects.create()
        chars = 'abcdefghijklmnopqrstuvwxyz'
        obj = LowercaseSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.islower() and obj.slug.isalpha())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_is_digits(self):
        """Test to make sure slug only contains digits."""
        DigitsSlug.objects.create()
        chars = '0123456789'
        obj = DigitsSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isdigit())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_has_no_vowels(self):
        """Test to make sure slug contains no vowels."""
        NoVowelSlug.objects.create()
        chars = 'aeiouAEIOU'
        obj = NoVowelSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isalnum())
        for char in obj.slug:
            self.assertFalse(char in chars)

    def test_max_slug_limit(self):
        """Test to make sure slug generation stops when there isn't any
        possible slugs remaining.
        """
        for _ in range(10):
            MaxSlugs.objects.create()
        self.assertRaises(FieldError, MaxSlugs.objects.create)

    def test_slugs_are_unique(self):
        """Test to make sure all slugs generated are unique."""
        for _ in range(10):
            MaxSlugs.objects.create()
        control = MaxSlugs.objects.get(pk=1)
        queryset = MaxSlugs.objects.all().exclude(pk=1)
        for obj in queryset:
            self.assertNotEqual(obj.slug, control.slug)

    def test_max_length(self):
        """Test to make sure max_length is correctly set."""
        field = RandomSlugField(length=10, max_length=255)
        self.assertEqual(field.max_length, 255)

    def test_max_length_defaults_to_length(self):
        field = RandomSlugField(length=10)
        self.assertEqual(field.max_length, 10)

    @skipIf(django.VERSION[:2] <= (1, 6),
            "Migrations are handled by south in Django < 1.7")
    def test_django_migrations(self):
        """Test that django migrations contain correct kwargs."""
        # Test exclude_upper and exclude_lower.
        old = RandomSlugField(length=9, exclude_upper=True, exclude_lower=True)
        name, path, args, kwargs = old.deconstruct()
        new = RandomSlugField(*args, **kwargs)
        self.assertEqual(old.length, new.length)
        self.assertEqual(old.exclude_upper, new.exclude_upper)
        self.assertEqual(old.exclude_lower, new.exclude_lower)

        # Test exclude_digits and exclude_vowels.
        old = RandomSlugField(length=7, exclude_digits=True,
                              exclude_vowels=True)
        name, path, args, kwargs = old.deconstruct()
        new = RandomSlugField(*args, **kwargs)
        self.assertEqual(old.length, new.length)
        self.assertEqual(old.exclude_digits, new.exclude_digits)
        self.assertEqual(old.exclude_vowels, new.exclude_vowels)
