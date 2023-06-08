from setuptools import setup

setup(
    name='Kitman',
    version='0.0.1',
    description='Utilities for Soccer Related Projects',
    author='Alejandro Cartas',
    author_email='alejandro.cartas@upf.edu',
    license='BSD 2-clause',
    packages=['kitman'],
    install_requires=['numpy>=1.23.5',
                      'opencv-python>=4.7.0.68',
                      'scikit-image>=0.19.3'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
    ],
)    
