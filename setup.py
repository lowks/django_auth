from setuptools import Command, setup


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='kagiso_django_auth',
    version='0.1',
    url='https://github.com/Kagiso-Future-Media/django_auth',
    cmdclass={'test': PyTest},
    install_requires=[
            'jsonfield==1.0.3',
            'requests==2.6.0',
    ],
)
