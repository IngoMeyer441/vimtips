import os
import runpy
import subprocess
from setuptools import setup, find_packages
from distutils.command.build import build

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None


class CustomBuild(build):
    def run(self):
        build.run(self)
        subprocess.check_call(["make"], cwd="./build/lib/vimtips/unblank_check")


if bdist_wheel is not None:

    class CustomBdistWheel(bdist_wheel):
        def finalize_options(self):
            bdist_wheel.finalize_options(self)
            self.root_is_pure = False  # force the build of platform specific wheels


else:
    CustomBdistWheel = None


def get_version_from_pyfile(version_file="vimtips/_version.py"):
    file_globals = runpy.run_path(version_file)
    return file_globals["__version__"]


def get_long_description_from_readme(readme_filename="README.md"):
    long_description = None
    if os.path.isfile(readme_filename):
        with open(readme_filename, "r", encoding="utf-8") as readme_file:
            long_description = readme_file.read()
    return long_description


version = get_version_from_pyfile()
long_description = get_long_description_from_readme()

setup(
    name="vimtips",
    version=version,
    packages=find_packages(),
    python_requires="~=3.3",
    install_requires=["PyQt5", "pyquery", "requests", "psutil"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["vimtips = vimtips.cli:main", "vimtips-daemon = vimtips.unblank_daemon:main"],
        "gui_scripts": ["vimtips-gui = vimtips.gui:main"],
    },
    cmdclass={"build": CustomBuild, "bdist_wheel": CustomBdistWheel},
    author="Ingo Meyer",
    author_email="IJ_M@gmx.de",
    description="Vim Tips is a project to aggregate and show vim tips from different sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/IngoMeyer441/vimtips",
    keywords=["vim", "tips"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Text Editors",
        "Topic :: Utilities",
    ],
)
