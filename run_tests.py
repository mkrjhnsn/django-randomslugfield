import sys

import django
from django.conf import settings


def main():
    settings.configure(
        INSTALLED_APPS=[
            'randomslugfield',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
    )

    # Setup django enviroment for standalone tests in django 1.7+
    # to prevent RuntimeError: App registry isn't ready yet.
    if django.VERSION[:2] >= (1, 7):
        django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['randomslugfield'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
