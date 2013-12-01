import sys

from django.conf import settings
from django.test.utils import get_runner


def main():
    settings.configure(
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        INSTALLED_APPS=[
            'randomslugfield',
        ],
    )

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['randomslugfield'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
