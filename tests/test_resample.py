import numpy as np
import pandas as pd
import polars as pl
import pytest

from camminapy.data import (
    resample_dataframe_grouped_pandas,
    resample_dataframe_grouped_polars,
    resample_dataframe_pandas,
    resample_dataframe_polars,
)

COMBINATIONS = [(10, 1), (20, 1), (300, 23)]


def _get_df_pandas(n, step, to_group: bool = False) -> pd.DataFrame:
    np.random.seed(1)
    x = list(range(0, n, step))
    y = np.random.randn(len(x))
    z = np.random.randn(len(x))
    grp = [1] * len(x)
    df1 = pd.DataFrame({"x": x, "y": y, "z": z, "grp": grp})
    if not to_group:
        return df1

    x = list(range(0, n, step))
    y = np.random.randn(len(x))
    z = np.random.randn(len(x))
    grp = [2] * len(x)
    df2 = pd.DataFrame({"x": x, "y": y, "z": z, "grp": grp})

    return pd.concat([df1, df2], ignore_index=True)


def _get_df_polars(n: int, step: int, to_group: bool = False) -> pl.DataFrame:
    return pl.DataFrame(_get_df_pandas(n, step, to_group))


@pytest.mark.parametrize("n,step", COMBINATIONS)
def test_reproduce_original_df_pandas(n: int, step: int):
    df = _get_df_pandas(n, step)
    df_resampled = resample_dataframe_pandas(
        df, interpolation_column="x", interpolation_step=step
    )

    assert df.equals(df_resampled)


@pytest.mark.parametrize("n,step", COMBINATIONS)
def test_reproduce_original_df_polars(n: int, step: int):
    df = _get_df_polars(n, step)
    df_resampled = resample_dataframe_polars(
        df, interpolation_column="x", interpolation_step=step
    )

    assert df.frame_equal(df_resampled)


@pytest.mark.parametrize("n,step", COMBINATIONS)
def test_reproduce_original_df_grouped_pandas(n: int, step: int):
    df = _get_df_pandas(n, step, to_group=True)
    df_resampled = resample_dataframe_grouped_pandas(
        df, interpolation_column="x", interpolation_step=step, group_column="grp"
    )

    assert df.equals(df_resampled)


@pytest.mark.parametrize("n,step", COMBINATIONS)
def test_reproduce_original_df_grouped_polars(n: int, step: int):
    df = _get_df_polars(n, step, to_group=True)
    df_resampled = resample_dataframe_grouped_polars(
        df, interpolation_column="x", interpolation_step=step, group_column="grp"
    )

    assert df.frame_equal(df_resampled)


@pytest.mark.parametrize("n,step", COMBINATIONS)
def test_reproduce_original_df_grouped_but_has_no_group_pandas(n: int, step: int):
    df = _get_df_pandas(n, step, to_group=False)
    df_resampled = resample_dataframe_grouped_pandas(
        df, interpolation_column="x", interpolation_step=step, group_column="grp"
    )

    assert df.equals(df_resampled)


@pytest.mark.parametrize("n,step", COMBINATIONS)
def test_reproduce_original_df_grouped_but_has_no_group_polars(n: int, step: int):
    df = _get_df_polars(n, step, to_group=False)
    df_resampled = resample_dataframe_grouped_polars(
        df, interpolation_column="x", interpolation_step=step, group_column="grp"
    )

    assert df.frame_equal(df_resampled)


def test_correctly_treat_string_cols():
    df = pd.DataFrame({"t": [1, 2, 3], "y": [10, 20, 30], "z": ["dog", "dog", "dog"]})
    df2 = resample_dataframe_pandas(df, interpolation_column="t", interpolation_step=1)
    assert df.equals(df2)


def test_correctly_treat_string_cols_grps():
    df = pd.DataFrame(
        {
            "t": [1, 2, 3, 4],
            "y": [10, 20, 30, 22],
            "z": ["dog", "dog", "cat", "cat"],
            "grp": ["A", "A", "B", "B"],
        }
    )
    df2 = resample_dataframe_grouped_pandas(
        df, interpolation_column="t", interpolation_step=1, group_column="grp"
    )
    assert df.equals(df2)
