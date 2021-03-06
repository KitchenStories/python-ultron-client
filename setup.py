from setuptools import setup

setup(
    name='ultron client',
    version='0.1.0',
    description='Python Ultron async Client',
    author='Trung Phan',
    packages=['ultron_client'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'requests_futures'
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
