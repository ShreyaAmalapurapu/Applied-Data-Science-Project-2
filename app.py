from pathlib import Path
import pandas as pd
from shiny import reactive
from shiny.express import input, render, ui
from data_cleansing import normalize_dataframe, parse_uploaded_file

# ----------------------------
# App settings
# ----------------------------
ui.page_opts(title="Upload Page Test", fillable=True)

app_dir = Path(__file__).resolve().parent

# ----------------------------
# Shared reactive values
# ----------------------------
current_df = reactive.value(pd.DataFrame())

data_source_info = reactive.value({
    "source_type": None,
    "source_name": None
})

# ---------------------------- Page1_upload data ----------------------------

# ----------------------------
# Helper functions
# ----------------------------
def load_sample_dataset(name: str) -> pd.DataFrame:
    if name == "penguins":
        return pd.read_csv(app_dir / "penguins.csv")

    elif name == "iris":
        return pd.DataFrame({
            "sepal_length": [5.1, 4.9, 4.7, 4.6, 5.0],
            "sepal_width": [3.5, 3.0, 3.2, 3.1, 3.6],
            "petal_length": [1.4, 1.4, 1.3, 1.5, 1.4],
            "petal_width": [0.2, 0.2, 0.2, 0.2, 0.2],
            "species": ["setosa", "setosa", "setosa", "setosa", "setosa"]
        })

    return pd.DataFrame()


# ----------------------------
# Navigation
# ----------------------------
with ui.nav_panel("Data Upload"):
    with ui.layout_columns(col_widths=(4, 8)):
        with ui.card():
            ui.h3("Data Upload")
            ui.markdown("Choose a sample dataset or upload your own file. (accepted formats: .csv, .xlsx, .json, .rds)")

            ui.input_radio_buttons(
                "data_source",
                "Choose source",
                choices={
                    "sample": "Sample dataset",
                    "upload": "Upload file"
                },
                selected="sample"
            )

            ui.input_select(
                "sample_dataset",
                "Sample dataset",
                choices={
                    "penguins": "Penguins",
                    "iris": "Iris"
                },
                selected="penguins"
            )

            ui.input_file(
                "file_upload",
                "Upload file",
                accept=[".csv", ".xlsx", ".json", ".rds"],
                multiple=False
            )

        with ui.card():
            ui.h3("Status")

            @render.text
            def status_text():
                df = current_df.get()
                info = data_source_info.get()

                if info.get("source_type") == "upload_failed":
                    return f"Upload failed: {info.get('source_name')}"

                if df.empty:
                    return "No data loaded yet."

                return (
                    f"Loaded successfully | "
                    f"Source: {info.get('source_type')} | "
                    f"Name: {info.get('source_name')} | "
                    f"Shape: {df.shape[0]} rows × {df.shape[1]} columns"
                )

    with ui.navset_tab():
        with ui.nav_panel("Summary"):
            @render.table
            def summary_table():
                df = current_df.get()

                if df.empty:
                    return pd.DataFrame({"Message": ["No data loaded"]})

                return pd.DataFrame({
                    "Metric": [
                        "Rows",
                        "Columns",
                        "Missing Values",
                        "Duplicate Rows",
                        "Numeric Columns",
                        "Non-numeric Columns"
                    ],
                    "Value": [
                        df.shape[0],
                        df.shape[1],
                        int(df.isna().sum().sum()),
                        int(df.duplicated().sum()),
                        int(df.select_dtypes(include="number").shape[1]),
                        int(df.select_dtypes(exclude="number").shape[1])
                    ]
                })

        with ui.nav_panel("Preview"):
            @render.data_frame
            def preview_table():
                df = current_df.get()

                if df.empty:
                    return render.DataGrid(
                        pd.DataFrame({"Message": ["No data loaded"]}),
                        width="100%"
                    )

                return render.DataGrid(df.head(10), width="100%")

        with ui.nav_panel("Columns"):
            @render.table
            def column_info():
                df = current_df.get()

                if df.empty:
                    return pd.DataFrame({"Message": ["No data loaded"]})

                return pd.DataFrame({
                    "Column": df.columns,
                    "Type": [str(dtype) for dtype in df.dtypes],
                    "Missing": [int(df[col].isna().sum()) for col in df.columns],
                    "Unique": [int(df[col].nunique(dropna=True)) for col in df.columns]
                })

        with ui.nav_panel("Structure"):
            ui.h4("Dataset Structure")

            @render.ui
            def structure_summary():
                df = current_df.get()

                if df.empty:
                    return ui.p("No data loaded.")

                return ui.TagList(
                    ui.p(f"Rows: {df.shape[0]}"),
                    ui.p(f"Columns: {df.shape[1]}")
                )

            @render.table
            def structure_table():
                df = current_df.get()

                if df.empty:
                    return pd.DataFrame({"Message": ["No data loaded"]})

                return pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": [str(df[col].dtype) for col in df.columns]
                })

with ui.nav_panel("Page 2"):
    ui.markdown("This is page 2.")


# ----------------------------
# Reactive logic
# ----------------------------
@reactive.effect
@reactive.event(input.data_source, input.sample_dataset)
def _load_sample():
    if input.data_source() != "sample":
        return

    df = normalize_dataframe(load_sample_dataset(input.sample_dataset()))

    current_df.set(df)
    data_source_info.set({
        "source_type": "sample",
        "source_name": input.sample_dataset()
    })


@reactive.effect
@reactive.event(input.file_upload)
def _load_upload():
    if input.data_source() != "upload":
        return

    files = input.file_upload()
    if not files:
        return

    fileinfo = files[0]

    try:
        df = parse_uploaded_file(fileinfo)

        current_df.set(df)
        data_source_info.set({
            "source_type": "upload",
            "source_name": fileinfo["name"]
        })

    except Exception as e:
        current_df.set(pd.DataFrame())
        data_source_info.set({
            "source_type": "upload_failed",
            "source_name": str(e)
        })