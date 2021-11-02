import sys, os
sys.path.insert(1, os.getcwd())

import hello_world

def test_hello_world():
    assert hello_world.function1() == 1