import src.hello_world


def test_hello_world(capsys):
    src.hello_world.main()
    captured = capsys.readouterr()
    src.hello_world.foo(1.5)
    assert captured.out == "Hello world!\n"
