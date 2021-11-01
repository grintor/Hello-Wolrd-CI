from pylint.lint import Run
from glob import glob
import warnings

def test_pylint_main(capsys):
    for file in glob("*.py", recursive=True):
        for rcfile in ['additional', 'main']:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                results = Run([f'--rcfile=lint_{rcfile}.rc', file], exit=False)
            assert results.linter.stats['error'] == 0 
            assert results.linter.stats['fatal'] == 0

            if 'global_note' in results.linter.stats:
                assert results.linter.stats['global_note'] > 0

                if results.linter.stats['global_note'] < 9:
                    # run it again, but this time show the output and then raise a warning.
                    with capsys.disabled():
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                        Run([f'--rcfile=lint_{rcfile}.rc', file], exit=False)
                    warnings.warn(UserWarning(f'LOW QUALITY CODE DETECTED IN "{file}". CONSIDER REVISING'))


if __name__ == "__main__":
    print('run tests using "pytest" command')
