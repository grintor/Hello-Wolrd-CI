from pylint.lint import Run
from glob import glob
import json
from pylint.reporters.text import TextReporter
import io


def main():
    scores = []

    with open(".repo-reports/pylint-problems.txt", "w+", encoding="utf-8") as f:
        f.truncate()

    for file in glob("**/*.py", recursive=True):
        if not file.startswith(("tests", ".repo-tools")):

            with io.StringIO() as f:
                results = Run(
                    [file, "--score=n"],
                    reporter=TextReporter(f),
                    exit=False,
                )
                report = f.getvalue()

            if results.linter.stats.global_note:
                score = results.linter.stats.global_note
                scores.append(score)
                if score < 10:
                    problems_path = ".repo-reports/pylint-problems.txt"
                    with open(problems_path, "a", encoding="utf-8", newline="\n") as f:
                        f.write(report)

    average_score = round(sum(scores) / len(scores), 1)

    score_color = "red"
    if average_score > 9:
        score_color = "yellow"
    if average_score > 9.5:
        score_color = "#34D058"

    shield_path = ".repo-shields/quality_shield.json"
    with open(shield_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "label": "Code Quality",
                    "message": f"{average_score}/10",
                    "color": score_color,
                },
                indent=4,
            )
        )
        f.write("\n")

    return average_score


def test_quality():
    assert main() > 9


if __name__ == "__main__":
    main()
