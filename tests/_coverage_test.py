import json
import subprocess
import os


def main():
    subprocess.run(["coverage", "erase"])
    subprocess.run(
        [
            "coverage",
            "run",
            "--omit=tests/*,.repo-tools/*",
            "-m",
            "pytest",
            f"--ignore={__file__}",
        ]
    )
    subprocess.run(
        ["coverage", "json", "-o", ".repo-reports/coverage.json", "--pretty-print"]
    )
    subprocess.run(["coverage", "html", "-d", ".repo-reports/coverage"])

    report_process = subprocess.run(["coverage", "report"], capture_output=True)
    with open(".repo-reports/coverage.txt", "w", encoding="utf-8", newline="\n") as f:
        for line in report_process.stdout.decode("utf-8").splitlines():
            f.write(f"{line}\n")
    subprocess.run(["coverage", "erase"])

    with open(".repo-reports/coverage.json", "r", encoding="utf-8") as f:
        coverage_result = json.loads(f.read())

    os.unlink(".repo-reports/coverage.json")

    percent_covered = round(coverage_result["totals"]["percent_covered"])

    covered_color = "red"
    if percent_covered > 95:
        covered_color = "yellow"
    if percent_covered > 98:
        covered_color = "#34D058"

    shield_path = ".repo-shields/covered_shield.json"
    with open(shield_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "label": "Test Coverage",
                    "message": f"{percent_covered}%",
                    "color": covered_color,
                },
                indent=4,
            )
        )
        f.write("\n")

    return percent_covered


def test_coverage():
    assert main() > 90


if __name__ == "__main__":
    main()
