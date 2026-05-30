from setuptools import setup, find_packages

setup(
    name="terminal-fun",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "pygame",
    ],
    entry_points={
        "console_scripts": [
            "donut=terminal_fun.donut:run_donut",
            "bad-apple=terminal_fun.bad_apple:run_bad_apple",
            "lotm=terminal_fun.lotm:run_lotm",
        ],
    },
    author="Arvioss",
    description="Terminal animations: Donut, Bad Apple, and LOTM",
)
