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
    def setUp(self):
        self.lower = 'abcdefghijklmnopqrstuvwxyz'
        self.upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.digits = '0123456789'
        self.vowels = 'aeiouAEIOU'

        FullSlug.objects.create()
        LowercaseSlug.objects.create()
        UppercaseSlug.objects.create()
        DigitsSlug.objects.create()
        NoVowelSlug.objects.create()
        for _ in range(10):
            MaxSlugs.objects.create()

    def test_slug_length(self):
        '''Test to make sure slug is correct length.'''
        obj = FullSlug.objects.get(pk=1)
        self.assertEqual(len(obj.slug), 255)

    def test_slug_charset(self):
        '''Test to make sure slug only contains ascii characters and
        digits.
        '''
        chars = self.upper + self.lower + self.digits
        obj = FullSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isalnum())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_is_uppercase(self):
        '''Test to make sure slug only contains uppercase characters.'''
        chars = self.upper
        obj = UppercaseSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isupper() and obj.slug.isalpha())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_is_lowercase(self):
        '''Test to make sure slug only contains lowercase characters.'''
        chars = self.lower
        obj = LowercaseSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.islower() and obj.slug.isalpha())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_is_digits(self):
        '''Test to make sure slug only contains digits.'''
        chars = self.digits
        obj = DigitsSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isdigit())
        for char in obj.slug:
            self.assertTrue(char in chars)

    def test_slug_has_no_vowels(self):
        '''Test to make sure slug contains no vowels.'''
        chars = self.vowels
        obj = NoVowelSlug.objects.get(pk=1)
        self.assertTrue(obj.slug.isalnum())
        for char in obj.slug:
            self.assertFalse(char in chars)

    def test_max_slug_limit(self):
        '''Test to make sure slug generation stops when there isn't any
        possible slugs remaining.
        '''
        self.assertRaises(FieldError, MaxSlugs.objects.create)

    def test_slugs_are_unique(self):
        '''Test to make sure all slugs generated are unique.'''
        control = MaxSlugs.objects.get(pk=1)
        queryset = MaxSlugs.objects.all().exclude(pk=1)
        for obj in queryset:
            self.assertNotEqual(obj.slug, control.slug)
