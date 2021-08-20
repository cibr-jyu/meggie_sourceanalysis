from setuptools import setup

setup(
    name='meggie_sourceanalysis',
    version='0.2.1',
    license='BSD',
    packages=['meggie_sourceanalysis'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'meggie>=1.3.0',
        'mayavi',
        'pysurfer'
    ]
)
