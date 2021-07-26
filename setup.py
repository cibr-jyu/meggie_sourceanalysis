from setuptools import setup

setup(
    name='meggie_sourceanalysis',
    version='0.2.0',
    license='BSD',
    packages=['meggie_sourceanalysis'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'meggie==1.1.1'
    ]
)
