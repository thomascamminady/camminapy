from camminapy.plot import altair_setup, altair_theme
from camminapy.plot.altair_theme import (
    altair_theme_gray,
    altair_theme_gray_label_in_plot,
)


def test_theme_does_not_cause_crash():
    altair_theme()
    assert True


def test_setup_does_not_cause_crash():
    altair_setup()
    assert True


def test_theme_returns_dict_gray():
    assert isinstance(altair_theme_gray(), dict)


def test_theme_returns_dict_gray_label_in_plot():
    assert isinstance(altair_theme_gray_label_in_plot(), dict)
