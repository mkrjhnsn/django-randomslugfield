import re

from django.core.exceptions import FieldError
from django.db.models import SlugField
from django.utils.crypto import get_random_string


class RandomSlugField(SlugField):

    """Generates a random ascii based slug eg. www.example.com/kEwD58P

    By default sets editable=False, blank=True, and unique=True.

    Required arguments:

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

    def __init__(self, length=None, exclude_upper=False, exclude_lower=False,
                 exclude_digits=False, exclude_vowels=False, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)

        if length is None:
            raise ValueError("Missing 'length' argument.")
        elif exclude_lower and exclude_upper and exclude_digits:
            raise ValueError("Cannot exclude all valid characters.")
        else:
            self.length = length
            self.exclude_upper = exclude_upper
            self.exclude_lower = exclude_lower
            self.exclude_digits = exclude_digits
            self.exclude_vowels = exclude_vowels

        self.chars = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                      '0123456789')
        if self.exclude_upper:
            self.chars = self.chars.replace('ABCDEFGHIJKLMNOPQRSTUVWXYZ', '')
        if self.exclude_lower:
            self.chars = self.chars.replace('abcdefghijklmnopqrstuvwxyz', '')
        if self.exclude_digits:
            self.chars = self.chars.replace('0123456789', '')
        if self.exclude_vowels:
            self.chars = re.sub(r'[aeiouAEIOU]', '', self.chars)

        kwargs.setdefault('max_length', self.length)
        if kwargs['max_length'] < self.length:
            raise ValueError("'max_length' must be equal to or greater than "
                             "'length'.")

        super(RandomSlugField, self).__init__(*args, **kwargs)

    def generate_slug(self, model_instance):
        """Returns a unique slug."""
        queryset = model_instance.__class__._default_manager.all()

        if queryset.count() >= len(self.chars)**self.length:
            raise FieldError("No available slugs remaining.")

        slug = get_random_string(self.length, self.chars)

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
            slug = get_random_string(self.length, self.chars)
            kwargs[self.attname] = slug

        return slug

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_slug(model_instance)
            setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(RandomSlugField, self).deconstruct()
        kwargs['length'] = self.length
        # Only include kwarg if it's not the default
        if self.exclude_upper:
            kwargs['exclude_upper'] = True
        if self.exclude_lower:
            kwargs['exclude_lower'] = True
        if self.exclude_digits:
            kwargs['exclude_digits'] = True
        if self.exclude_vowels:
            kwargs['exclude_vowels'] = True
        return name, path, args, kwargs

    def south_field_triple(self):
        """Returns a suitable description of this field for South."""
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = '%s.%s' % (self.__module__, self.__class__.__name__)
        args, kwargs = introspector(self)
        kwargs.update({
            'length': repr(self.length),
            'exclude_upper': repr(self.exclude_upper),
            'exclude_lower': repr(self.exclude_lower),
            'exclude_digits': repr(self.exclude_digits),
            'exclude_vowels': repr(self.exclude_vowels),
        })
        # That's our definition!
        return (field_class, args, kwargs)
