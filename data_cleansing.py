from pathlib import Path

import pandas as pd
import pyreadr


ACCEPTED_EXTENSIONS = {".csv", ".xlsx", ".json", ".rds"}


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with normalized column names for analysis."""
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    if df.empty:
        return df

    normalized = df.copy()
    normalized.columns = [str(col).strip() for col in normalized.columns]
    return normalized


def handle_null_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values so the DataFrame is usable for analysis.

    Rules:
    - Drop rows/columns that are completely null.
    - Fill numeric nulls with column median.
    - Fill non-numeric nulls with "Unknown".
    """
    if df.empty:
        return df

    cleaned = df.copy()
    cleaned = cleaned.dropna(axis=0, how="all").dropna(axis=1, how="all")

    if cleaned.empty:
        return cleaned

    numeric_columns = cleaned.select_dtypes(include="number").columns
    for col in numeric_columns:
        if cleaned[col].isna().any():
            median_value = cleaned[col].median()
            fill_value = median_value if pd.notna(median_value) else 0
            cleaned[col] = cleaned[col].fillna(fill_value)

    non_numeric_columns = cleaned.select_dtypes(exclude="number").columns
    for col in non_numeric_columns:
        if cleaned[col].isna().any():
            cleaned[col] = cleaned[col].fillna("Unknown")

    return cleaned


def _read_rds(path: str) -> pd.DataFrame:
    """Read an RDS file and convert the first object to DataFrame."""
    result = pyreadr.read_r(path)
    if not result:
        return pd.DataFrame()

    first_key = next(iter(result.keys()))
    obj = result[first_key]
    if isinstance(obj, pd.DataFrame):
        return obj
    return pd.DataFrame(obj)


def parse_uploaded_file(fileinfo: dict) -> pd.DataFrame:
    """
    Parse uploaded fileinfo dict from Shiny input_file and return DataFrame.

    Expected fileinfo keys:
    - datapath: temp file path
    - name: original filename
    """
    path = str(fileinfo["datapath"])
    name = str(fileinfo["name"])
    ext = Path(name).suffix.lower()

    if ext not in ACCEPTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {ext}. "
            f"Supported formats: {', '.join(sorted(ACCEPTED_EXTENSIONS))}"
        )

    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".xlsx":
        df = pd.read_excel(path, engine="openpyxl")
    elif ext == ".json":
        df = pd.read_json(path)
    else:  # .rds
        df = _read_rds(path)

    normalized = normalize_dataframe(df)
    return handle_null_data(normalized)
