from setuptools import setup, find_packages

setup(
    name='bad-apples',
    version='1.0.0',
    description='Get a random quote',
    url='http://github.com/nerdraven/bad-apples',
    author='Damian Akpan',
    author_email='damianakpan2001@gmail.com',
    license='MIT',
    install_requires=['psutil'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['bad_apples=src.bad_apples:main']
    )
)
