'''pylint sucks'''
import functions.echo

def test_echo():
    assert functions.echo.echo("1") == "1", "1 == 1"
    assert functions.echo.echo("abc") == "abc", "abc == abc"
    assert functions.echo.echo("trump") == "trump", "trump == trump"
