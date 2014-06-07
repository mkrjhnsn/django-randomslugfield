from setuptools import setup

setup(
    name="django-randomslugfield",
    version="0.3.0",
    author="Mike Johnson",
    author_email="mkrjhnsn@gmail.com",
    packages=['randomslugfield'],
    url="http://github.com/mkrjhnsn/django-randomslugfield",
    license="MIT",
    description="A Django field that automatically generates random slugs.",
    long_description="Generates unique random slugs using these characters "
                     "`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     "0123456789`. See the project page for more information: "
                     "http://github.com/mkrjhnsn/django-randomslugfield",
    tests_require=['django'],
    test_suite='run_tests.main',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)
