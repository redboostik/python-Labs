from setuptools import setup

setup(
    name='dump_library',
    packages=[
        'dump_library',
        'dump_library/parsers',
        'dump_library/parsers/Json',
        'dump_library/parsers/TOML',
        'dump_library/parsers/YAML',
    ],
    version='1.0.3',
    author='redboostik',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.3'],
    test_suite='tests',
    scripts=['dump_library/dump_console.py']
)