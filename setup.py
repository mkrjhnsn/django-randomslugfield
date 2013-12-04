from setuptools import setup

setup(
    name="django-randomslugfield",
    version="0.2.0",
    author="Michael Johnson",
    author_email="mkrjhnsn@gmail.com",
    packages=['randomslugfield'],
    url="http://github.com/melinko/django-randomslugfield",
    license="MIT",
    description="A Django field that automatically generates random slugs.",
    long_description="Generates unique random slugs using these characters " \
        "`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`.",
    tests_require=['django'],
    test_suite='run_tests.main',
)
