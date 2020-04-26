from setuptools import setup

from test_code_style_checker import __version__

setup(
    name='test_code_style_checker',
    version=__version__,
    description="flake8 plugin",
    long_description='long description',
    author="tolstislon",
    author_email='tolstislon@gmail.com',
    url='https://github.com/tolstislon/test_code_style_checker',
    entry_points={
        'flake8.extension': [
            'MC = test_code_style_checker:CheckerTestFile',
        ],
    },
    packages=['test_code_style_checker'],
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.8',
    license="MIT License",
    zip_safe=False,
    keywords='flake8 test_code_style_checker',
    classifiers=[
        'Framework :: Flake8',
        'Intended Audience :: Developers'
    ]
)
