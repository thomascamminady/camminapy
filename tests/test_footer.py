import os

import altair as alt

from camminapy.plot import Footer


def test_footer_returns_subtitle_dict():
    path = os.getcwd()
    chart = alt.Chart().properties(
        title={"text": "ACTUAL PLOT TITLE", **Footer(path).subtitle()}
    )
    assert isinstance(chart, alt.Chart)


def test_footer_can_create_chart():
    path = os.getcwd()

    chart = alt.Chart().properties(title=Footer(path).create())
    assert isinstance(chart, alt.Chart)


def test_footer_returns_subtitle_dict_no_path():
    chart = alt.Chart().properties(
        title={"text": "ACTUAL PLOT TITLE", **Footer().subtitle()}
    )
    assert isinstance(chart, alt.Chart)


def test_footer_can_create_chart_no_path():
    chart = alt.Chart().properties(title=Footer().create())
    assert isinstance(chart, alt.Chart)


def test_footer_can_create_chart_no_path_not_one_line():
    chart = alt.Chart().properties(title=Footer().create(one_line=False))
    assert isinstance(chart, alt.Chart)
