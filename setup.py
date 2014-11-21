from setuptools import setup, find_packages
from version import get_git_version


setup(
    name='thecut-publishing',
    author='The Cut',
    author_email='development@thecut.net.au',
    url='http://projects.thecut.net.au/projects/thecut-publishing',
    namespace_packages=['thecut'],
    version=get_git_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-tagging==0.3.1',  # Required to run south migrations.
                      'django-taggit==0.12'],
)
