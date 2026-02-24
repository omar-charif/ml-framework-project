import os
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from ml_framework_project.data_analyzer.data_reader import (
    read_csv,
    read_excel,
    read_json,
    read_parquet,
    read_data,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})


def test_read_csv_reads_dataframe(tmp_path, sample_df):
    p = tmp_path / "test.csv"
    sample_df.to_csv(p, index=False)

    out = read_csv(str(p))

    assert_frame_equal(out.reset_index(drop=True), sample_df.reset_index(drop=True))


def test_read_json_reads_dataframe(tmp_path, sample_df):
    p = tmp_path / "test.json"
    # write as array-of-objects which pandas.read_json can consume
    sample_df.to_json(p, orient="records")

    out = read_json(str(p))
    # read_json may infer types; ensure equality with relaxed dtype check
    assert_frame_equal(out.reset_index(drop=True), sample_df.reset_index(drop=True))


def test_read_nonexistent_returns_empty_dataframe():
    out = read_csv("nonexistent_file_hopefully_does_not_exist.csv")
    assert isinstance(out, pd.DataFrame)
    assert out.empty


def test_read_data_dispatch_csv_and_json(tmp_path, sample_df):
    csvp = tmp_path / "d.csv"
    jsonp = tmp_path / "d.json"
    sample_df.to_csv(csvp, index=False)
    sample_df.to_json(jsonp, orient="records")

    out_csv = read_data(str(csvp))
    out_json = read_data(str(jsonp))

    assert_frame_equal(out_csv.reset_index(drop=True), sample_df.reset_index(drop=True))
    assert_frame_equal(out_json.reset_index(drop=True), sample_df.reset_index(drop=True))


def test_read_data_unsupported_extension_returns_empty(tmp_path):
    p = tmp_path / "data.unknown"
    p.write_text("nothing")

    out = read_data(str(p))
    assert isinstance(out, pd.DataFrame)
    assert out.empty


def test_read_excel_if_engine_available(tmp_path, sample_df):
    pytest.importorskip("openpyxl")
    p = tmp_path / "test.xlsx"
    sample_df.to_excel(p, index=False)

    out = read_excel(str(p))
    assert_frame_equal(out.reset_index(drop=True), sample_df.reset_index(drop=True))


def test_read_parquet_if_engine_available(tmp_path, sample_df):
    # require either pyarrow or fastparquet to be installed for parquet IO
    pytest.importorskip("pyarrow")
    p = tmp_path / "test.parquet"
    sample_df.to_parquet(p)

    out = read_parquet(str(p))
    assert_frame_equal(out.reset_index(drop=True), sample_df.reset_index(drop=True))
