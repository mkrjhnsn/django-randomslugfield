import random
import string

from django.db.models import SlugField


class RandomSlugField(SlugField):
    """ RandomSlugField

    Generates a random ascii based slug eg. www.example.com/kEwD58P

    By default sets editable=False, blank=True, and unique=True.

    Requires arguments:

        length
            Specifies the length of the generated slug. (integer)

    Optional arguments:

        exclude_lower
            Boolean to exclude lowercase ascii characters. (default=False)

        exclude_upper
            Boolean to exclude uppercase ascii characters. (default=False)

        exclude_digits
            Boolean to exclude digits. (default=False)

    Inspired by django-extensions AutoSlugField:
    http://pythonhosted.org/django-extensions/
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)

        self.length = kwargs.pop('length', None)
        self.exclude_lower = kwargs.pop('exclude_lower', False)
        self.exclude_upper = kwargs.pop('exclude_upper', False)
        self.exclude_digits = kwargs.pop('exclude_digits', False)

        if self.length is None:
            raise ValueError("Missing 'length' argument.")
        elif not isinstance(self.length, int):
            raise TypeError("'length' argument is invalid type. Must be integer.")

        if self.exclude_lower and self.exclude_upper and self.exclude_digits:
            raise ValueError("Cannot exclude all valid characters.")

        kwargs['max_length'] = self.length

        self.valid_chars = string.ascii_letters + string.digits
        if self.exclude_lower:
            self.valid_chars =  self.valid_chars.replace(string.ascii_lowercase, '')
        if self.exclude_upper:
            self.valid_chars = self.valid_chars.replace(string.ascii_uppercase, '')
        if self.exclude_digits:
            self.valid_chars = self.valid_chars.replace(string.digits, '')

        super(RandomSlugField, self).__init__(*args, **kwargs)

    def generate_slug(self, model_instance):
        slug = ''.join(random.choice(self.valid_chars) for x in range(self.length))

        # Exclude the current model instance from the queryset used in
        # finding next valid hash.
        queryset = model_instance.__class__._default_manager.all()
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
            slug = ''.join(random.choice(self.valid_chars) for x in range(self.length))
            kwargs[self.attname] = slug

        return slug

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_slug(model_instance)
            setattr(model_instance, self.attname, value)

        return value

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = '%s.RandomSlugField' % self.__module__
        args, kwargs = introspector(self)
        kwargs.update({
            'length': repr(self.length),
            'exclude_lower': repr(self.exclude_lower),
            'exclude_upper': repr(self.exclude_upper),
            'exclude_digits': repr(self.exclude_digits),
        })
        # That's our definition!
        return (field_class, args, kwargs)
