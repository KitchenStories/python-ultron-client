from setuptools import setup

setup(
    name='Ultron Client',
    version='0.1.0',
    packages=['ultron_client'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'flask',
        'pytest',
        'requests',
        'requests_futures'
    ],
)
