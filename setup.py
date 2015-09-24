#! /usr/bin/env python

from setuptools import setup, find_packages
import glob, versioneer

setup (
    name = "qworker_sample",
    version = versioneer.get_version (),                
    description = "Sample plugin workerd for QWorkerD",
    long_description = file ("README.rst").read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [],
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    license = "LGPL v3.0",
    packages = find_packages (exclude = ["tests"]),
    package_data = {"qworker_sample": ["_cfgtool/qworker_sample",
                                      "_cfgtool/*.templ",
                                      "_cfgtool/install",],
    },
    data_files = [
        ("/etc/cfgtool/module.d/", ["qworker_sample/_cfgtool/qworker_sample",]),
        ("/etc/qworkerd", glob.glob ("qworker_sample/_cfgtool/*.templ")),
    ],
    zip_safe = False,
    install_requires = [line.strip ()
                        for line in file ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
