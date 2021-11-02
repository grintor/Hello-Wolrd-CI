from pylint.lint import Run
from glob import glob
import warnings, json

def test_pylint(capsys):
    scores = []
    for file in glob("**/*.py", recursive=True):
        if not file.startswith('tests'):
            for rcfile in ['additional', 'main']:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    results = Run([f'--rcfile=tests/conf/lint_{rcfile}.rc', '--output-format=parseable:tests/results/quality.txt', file], exit=False)
                assert results.linter.stats['error'] == 0 
                assert results.linter.stats['fatal'] == 0

                if 'global_note' in results.linter.stats:
                    score = round(results.linter.stats['global_note'], 2)
                    scores.append(score)
                    if score < 9:
                        # run it again, but this time show the output and then raise a warning.
                        with capsys.disabled():
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                            Run([f'--rcfile=tests/conf/lint_{rcfile}.rc', file], exit=False)
                        warnings.warn(UserWarning(f'LOW QUALITY CODE DETECTED IN "{file}". Score of {score}. CONSIDER REVISING'))

                    assert score > 1, 'Code quality must be above minimum threshold'

    average_score = round(sum(scores) / len(scores), 1)

    score_color = 'red'
    if average_score > 7:
        score_color = 'yellow'
    if average_score > 8:
        score_color = 'green'

    with open('tests/results/quality_shield.json', 'w') as f:
        f.write(json.dumps({
            'schemaVersion': 1,
            'label': 'code quality',
            'message': f'{average_score}/10',
            'color': score_color
        }))

if __name__ == "__main__":
    print('run tests using "pytest" command')
