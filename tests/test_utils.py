"""
Utility  tests
"""
from package_manager.utils import secho


def test_colors(capsys):
    secho("Hi", fg="blue", bg="orange", bold=True)
    captured = capsys.readouterr()
    assert captured.out == "\033[34m\033[43m\033[01mHi\033[0m\n"
