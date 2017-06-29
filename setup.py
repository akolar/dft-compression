from setuptools import setup


setup(
    name='dft',
    version='0.1',
    author='Anze Kolar',
    author_email='kolar.anze@gmail.com',
    license='MIT',
    packages=['dft'],
    entry_points={
        'console_scripts': [
            'dft=dft.__main__:main',
        ],
    },
    install_requires=[
        'matplotlib==2.0.2',
        'numpy==1.12.1',
        'Pillow==4.1.1',
        'scipy==0.19.0'
    ]
)
