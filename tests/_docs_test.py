import subprocess
import shutil


def main():
    shutil.rmtree(".repo-reports/docs-preview", ignore_errors=True)
    proc = subprocess.run(
        [
            "sphinx-build",
            "-W",
            "--keep-going",
            "-a",
            "-b",
            "html",
            "docs-src",
            ".repo-reports/docs-preview",
        ]
    )
    if proc.returncode != 0:
        return proc.returncode

    shutil.rmtree("docs", ignore_errors=True)
    proc = subprocess.run(
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
    return proc.returncode


def test_docs():
    assert main() == 0


if __name__ == "__main__":
    main()
