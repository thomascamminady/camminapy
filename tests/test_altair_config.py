from camminapy.plot import altair_setup, altair_theme


def test_theme_does_not_cause_crash():
    altair_theme()
    assert True


def test_setup_does_not_cause_crash():
    altair_setup()
    assert True
