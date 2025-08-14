from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class PostInstallCommand(install):

    def run(self):
        install.run(self)
        # Run post-install script
        try:
            subprocess.call(['python3', 'setup_postinstall.py'])
        except Exception as e:
            print(f"Warning: Post-install script failed: {e}")


setup(
    name='Liblouis-Table-Editor',
    version='1.0.0',
    description='A graphical editor for Liblouis Braille translation tables.',
    author='Sahil Rakhaiya',
    author_email='sahilrakhaiya05@gmail.com',
    url='https://github.com/SahilRakhaiya05/Liblouis-Table-Editor.git',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=requirements,
    package_data={
        '': [
            'assets/data/*.json',
            'assets/data/TestFiles/*',
            'assets/icons/*.png',
            'assets/icons/*.ico',
            'assets/images/*',
            'styles.qss',
            'tables/*.cti',
        ],
    },
    data_files=[
        ('share/applications', ['debian/liblouis-table-editor.desktop']),
        ('share/pixmaps', ['src/liblouis_table_editor/assets/icons/liblouis_table_editor.png']),
        ('share/mime/packages', ['debian/liblouis-table-editor.xml']),
    ],
    entry_points={
    'console_scripts': [
        'liblouis-table-editor = liblouis_table_editor.__main__:main'
    ],
},
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
