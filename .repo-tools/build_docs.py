import subprocess
import shutil


def main():
    shutil.rmtree("docs", ignore_errors=True)
    _ = subprocess.run(
        [
            "sphinx-build",
            "-W",
            "--keep-going",
            "-a",
            "-b",
            "dirhtml",
            "docs-src",
            "docs",
        ]
    )


if __name__ == "__main__":
    main()
