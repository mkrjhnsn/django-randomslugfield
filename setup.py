from distutils.core import setup

setup(
    name='django-randomslugfield',
    version='0.1.1',
    author='Mike Johnson',
    author_email='mkrjhnsn@gmail.com',
    packages=['randomslugfield'],
    url='http://github.com/melinko/django-randomslugfield',
    license='MIT',
    description='A Django field that automatically generates random slugs.',
    long_description=open('README.rst').read(),
)
