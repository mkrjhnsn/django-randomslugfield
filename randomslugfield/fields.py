import random
import re
import string

from django.core.exceptions import FieldError
from django.db.models import SlugField


class RandomSlugField(SlugField):
    """ RandomSlugField

    Generates a random ascii based slug eg. www.example.com/kEwD58P

    By default sets editable=False, blank=True, and unique=True.

    Requires arguments:

        length
            Specifies the length of the generated slug. (integer)

    Optional arguments:

        exclude_upper
            Boolean to exclude uppercase characters. (default=False)

        exclude_lower
            Boolean to exclude lowercase characters. (default=False)

        exclude_digits
            Boolean to exclude digits. (default=False)

        exclude_vowels
            Boolean to exclude vowels. (default=False)

    Inspired by django-extensions AutoSlugField:
    http://pythonhosted.org/django-extensions/
    """

    def __init__(self, length, exclude_upper=False, exclude_lower=False,
                 exclude_digits=False, exclude_vowels=False, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        self.length = length
        self.chars = self.generate_charset(exclude_upper=exclude_upper,
                                           exclude_lower=exclude_lower,
                                           exclude_digits=exclude_digits,
                                           exclude_vowels=exclude_vowels)

        kwargs['max_length'] = self.length
        super(RandomSlugField, self).__init__(*args, **kwargs)

    def generate_charset(self, exclude_upper, exclude_lower,
                         exclude_digits, exclude_vowels):
        if exclude_lower and exclude_upper and exclude_digits:
            raise ValueError("Cannot exclude all valid characters.")

        chars = string.ascii_letters + string.digits
        if exclude_upper:
            chars = chars.replace(string.ascii_uppercase, '')
        if exclude_lower:
            chars =  chars.replace(string.ascii_lowercase, '')
        if exclude_digits:
            chars = chars.replace(string.digits, '')
        if exclude_vowels:
            chars = re.sub(r'[aeiouAEIOU]', '', chars)
        return chars

    def generate_slug(self, model_instance):
        queryset = model_instance.__class__._default_manager.all()

        if queryset.count() >= len(self.chars)**self.length:
            raise FieldError("No available slugs remaining.")

        slug = ''.join(random.choice(self.chars) for _ in range(self.length))

        # Exclude the current model instance from the queryset used in
        # finding next valid slug.
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        # Form a kwarg dict used to impliment any unique_together
        # contraints.
        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)
        kwargs[self.attname] = slug

        while queryset.filter(**kwargs):
            slug = (''.join(random.choice(self.chars)
                    for _ in range(self.length)))
            kwargs[self.attname] = slug

        return slug

    def pre_save(self, model_instance, add):
        if add:
            value = self.generate_slug(model_instance)
            setattr(model_instance, self.attname, value)
            return value
        else:
            super(RandomSlugField, self).pre_save(model_instance, add)
