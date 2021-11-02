from pylint.lint import Run
from glob import glob
import warnings, json, subprocess, os

def test_coverage(capsys):
    subprocess.run(['coverage', 'erase'])
    for file in glob("tests/*.py", recursive=True):
        if not file.endswith('test_coverage.py') and not file.endswith('test_quality.py'):
            subprocess.run(['coverage', 'run', '-m', 'pytest', file])
            print(file)
    subprocess.run(['coverage', 'json', '-o', 'tests/results/coverage.json', '--pretty-print'])
    subprocess.run(['coverage', 'html', '-d', 'tests/results/coverage'])
    report_process = subprocess.run(['coverage', 'report'], capture_output=True)
    with open('tests/results/coverage.txt', 'wb') as f:
        f.write(report_process.stdout)
    subprocess.run(['coverage', 'erase'])
    
    with open('tests/results/coverage.json', 'r') as f:
        coverage_result = json.loads(f.read())

    os.unlink('tests/results/coverage.json')
    
    percent_covered = round(coverage_result['totals']['percent_covered'])

    covered_color = 'red'
    if percent_covered > 80:
        covered_color = 'yellow'
    if percent_covered > 90:
        covered_color = 'green'

    with open('tests/results/covered_shield.json', 'w') as f:
        f.write(json.dumps({
            'schemaVersion': 1,
            'label': 'coverage',
            'message': f'{percent_covered}%',
            'color': covered_color
        }))
    
    assert percent_covered > 70

if __name__ == "__main__":
    print('run tests using "pytest" command')
