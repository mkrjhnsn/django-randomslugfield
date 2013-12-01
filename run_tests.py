import sys

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

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['randomslugfield'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
