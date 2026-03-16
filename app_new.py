from pathlib import Path
import os
import pandas as pd
import pyreadr
from shiny import reactive
from shiny.express import input, render, ui
import matplotlib.pyplot as plt

app_dir = Path(__file__).resolve().parent
app_dir = app_dir / "sampledatasets"

current_df = reactive.value(pd.DataFrame())
data_source_info = reactive.value({
    "source_type": None,
    "source_name": None,
    "status": "idle",
    "message": "No data loaded yet."
})

# ui info

ui.tags.style("""
:root{
  --cds-blue: #B9D9EB;
  --cds-blue-soft: #EEF7FC;
  --cds-blue-deep: #89BDD8;
  --cds-text: #0F172A;
  --cds-muted: #475569;
  --cds-border: #D8E6EF;
  --cds-success-bg: #EAF7EE;
  --cds-success-text: #1E7A39;
  --cds-error-bg: #FDECEC;
  --cds-error-text: #B42318;
}

body {
  background: #F8FBFD;
  color: var(--cds-text);
  font-size: 16px;
}

.container-fluid, .container-xxl {
  max-width: 100% !important;
}

.product-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 10px 22px 10px;
  margin-bottom: 18px;
  border-bottom: 2px solid #E5EDF3;
}

.product-title {
  font-size: 48px;
  font-weight: 900;
  color: #000000;
  line-height: 1.05;
  letter-spacing: 0.2px;
}

.function-nav {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.function-item {
  font-size: 24px;
  font-weight: 700;
  color: #334155;
  padding: 8px 14px;
}

.function-divider {
  width: 1px;
  height: 28px;
  background: #B8C2CC;
}

.nav-tabs .nav-link {
  font-size: 20px !important;
  font-weight: 600 !important;
  padding: 10px 16px !important;
}

.card, .upload-card, .status-card, .content-card {
  border: 1.5px solid var(--cds-border) !important;
  border-radius: 22px !important;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
  padding: 12px;
}

.upload-title {
  font-size: 28px;
  font-weight: 400;
  color: #16324F;
  margin-bottom: 6px;
}

.upload-subtitle {
  font-size: 22px;
  color: var(--cds-muted);
  margin-bottom: 14px;
  line-height: 1.5;
}

.section-label {
  font-size: 22px;
  font-weight: 600;
  color: #1D4E89;
  margin-bottom: 10px;
}

.decor-block {
  background: linear-gradient(90deg, var(--cds-blue-soft), #ffffff);
  border-left: 7px solid var(--cds-blue-deep);
  padding: 12px 16px;
  border-radius: 16px;
  margin-bottom: 14px;
}

.status-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1F2937;
}

.status-box {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
}

.status-idle {
  background: #F1F5F9;
  color: #5B6470;
}

.status-success {
  background: var(--cds-success-bg);
  color: var(--cds-success-text);
}

.status-error {
  background: var(--cds-error-bg);
  color: var(--cds-error-text);
}

.form-label, .control-label {
  font-size: 24px !important;
  font-weight: 800 !important;
  color: #0F3D5E !important;
}

.shiny-input-container {
  margin-bottom: 18px !important;
}

.form-select, .form-control {
  font-size: 16px !important;
  min-height: 56px !important;
  border-radius: 14px !important;
}

.form-check-label {
  font-size: 22px !important;
  font-weight: 600 !important;
}

.form-check-input {
  transform: scale(1.35);
  margin-top: 0.35em;
}

.btn, .btn-default {
  font-size: 20px !important;
  border-radius: 14px !important;
  padding: 10px 18px !important;
}

.table {
  font-size: 20px !important;
}

.table th {
  font-size: 21px !important;
  font-weight: 800 !important;
}

.table td {
  font-size: 19px !important;
}

.bslib-gap-spacing {
  gap: 28px !important;
}
""")

with ui.div(class_="product-bar"):
    ui.div("Data Studio", class_="product-title")

# -----------------------------------------data upload_Page1-----------------------------------------
# load sample datasets
def load_sample_dataset(name: str) -> pd.DataFrame:
    if name == "penguins":
        return pd.read_csv(app_dir / "penguins.csv")

    elif name == "cars":
        return pd.read_json(app_dir / "cars.json")

    elif name == "College":
        result = pyreadr.read_r(app_dir / "College.rds")
        first_key = list(result.keys())[0]
        obj = result[first_key]
        return obj if isinstance(obj, pd.DataFrame) else pd.DataFrame(obj)

    else:
        raise ValueError(f"Unknown sample dataset: {name}")
    
def read_uploaded_file(fileinfo) -> pd.DataFrame:
    path = fileinfo["datapath"]
    name = fileinfo["name"]
    ext = os.path.splitext(name)[1].lower()

    if ext == ".csv":
        return pd.read_csv(path)
    elif ext == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")
    elif ext == ".json":
        return pd.read_json(path)
    elif ext == ".rds":
        result = pyreadr.read_r(path)
        first_key = list(result.keys())[0]
        obj = result[first_key]
        return obj if isinstance(obj, pd.DataFrame) else pd.DataFrame(obj)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

with ui.navset_tab():
    with ui.nav_panel("Data Upload"):
        with ui.layout_columns(col_widths=(5, 7)):
            with ui.card(class_="upload-card"):
                ui.div("Data Upload", class_="upload-title")
                ui.div(
                    "Choose a sample dataset or upload your own file.",
                    class_="upload-subtitle"
                )

                with ui.div(class_="decor-block"):
                    ui.div("Choose source", class_="section-label")
                    ui.input_radio_buttons(
                        "data_source",
                        None,
                        choices={
                            "sample": "Sample dataset",
                            "upload": "Upload file"
                        },
                        selected=None
                    )

                with ui.panel_conditional("input.data_source == 'sample'"):
                    with ui.div(class_="decor-block"):
                        ui.div("Sample dataset", class_="section-label")
                        ui.input_select(
                            "sample_dataset",
                            None,
                            choices={
                                "": "Please select a dataset",
                                "penguins": "Penguins (.csv)",
                                "cars": "cars (.json)",
                                "College": "College (.rds)"
                            },
                            selected=""
                        )

                with ui.panel_conditional("input.data_source == 'upload'"):
                    with ui.div(class_="decor-block"):
                        ui.div("Upload file", class_="section-label")
                        ui.input_file(
                            "file_upload",
                            None,
                            accept=[".csv", ".xlsx", ".json", ".rds"],
                            multiple=False
                        )
                                    

            with ui.div():
                with ui.card(class_="status-card"):
                    ui.div("Status", class_="status-title")

                    @render.ui
                    def status_ui():
                        info = data_source_info.get()
                        status = info["status"]
                        msg = info["message"]

                        if status == "success":
                            cls = "status-box status-success"
                        elif status == "error":
                            cls = "status-box status-error"
                        else:
                            cls = "status-box status-idle"

                        return ui.div(msg, class_=cls)

                ui.div(style="height: 4px;")

                with ui.card(class_="content-card"):
                    with ui.navset_tab():
                        with ui.nav_panel("Summary"):
                            @render.table
                            def summary_table():
                                df = current_df.get()
                                if df.empty:
                                    return pd.DataFrame({"Message": ["No data loaded"]})
                                return pd.DataFrame({
                                    "Metric": ["Rows", "Columns"],
                                    "Value": [df.shape[0], df.shape[1]]
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
                                    "Type": [str(dtype) for dtype in df.dtypes]
                                })

                        with ui.nav_panel("Structure"):
                            @render.table
                            def structure_table():
                                df = current_df.get()
                                if df.empty:
                                    return pd.DataFrame({"Message": ["No data loaded"]})
                                return pd.DataFrame({
                                    "Column": df.columns,
                                    "Missing": [int(df[col].isna().sum()) for col in df.columns],
                                    "Unique": [int(df[col].nunique(dropna=True)) for col in df.columns]
                                })
    # page for EDA
    with ui.nav_panel("Exploratory Data Analysis"):

        # Block 1: Dataset Summary
        with ui.card(class_="content-card"):
            ui.div("Dataset Summary", class_="status-title")


            @render.table
            def dataset_summary_table():
                df=current_df.get()

                if df.empty:
                    return pd.DataFrame({
                        "Metric": ["Message"],
                        "Value": ["No data loaded"]
                    })

                n_rows, n_cols=df.shape
                missing_cells=int(df.isna().sum().sum())
                duplicate_rows=int(df.duplicated().sum())
                numeric_cols=int(df.select_dtypes(include="number").shape[1])
                categorical_cols=int(df.select_dtypes(exclude="number").shape[1])

                return pd.DataFrame([
                    ("Rows", n_rows),
                    ("Columns", n_cols),
                    ("Missing Cells", missing_cells),
                    ("Duplicate Rows", duplicate_rows),
                    ("Numeric Columns", numeric_cols),
                    ("Categorical Columns", categorical_cols),
                ], columns=["Metric", "Value"])
        ui.br()

        # Block 2: Plot Controls
        with ui.card(class_="content-card"):
            ui.div("Visualization Controls", class_="status-title")

            with ui.layout_columns(col_widths=(4, 4, 4)):
                ui.input_select(
                    "plot_type",
                    "Choose plot type",
                    choices={
                        "scatter": "Scatter Plot",
                        "hist": "Histogram",
                        "box": "Box Plot",
                        "bar": "Bar Chart"
                    },
                    selected="scatter"
                )


                @render.ui
                def x_var_ui():
                    df=current_df.get()

                    if df.empty:
                        return ui.input_select(
                            "x_var",
                            "X variable",
                            choices={"": "No data loaded"},
                            selected=""
                        )

                    plot_type=input.plot_type()

                    if plot_type in ["scatter", "hist", "box"]:
                        cols=df.select_dtypes(include="number").columns.tolist()
                    else:
                        cols=df.columns.tolist()

                    if not cols:
                        return ui.input_select(
                            "x_var",
                            "X variable",
                            choices={"": "No valid columns"},
                            selected=""
                        )

                    return ui.input_select(
                        "x_var",
                        "X variable",
                        choices={col: col for col in cols},
                        selected=cols[0]
                    )


                @render.ui
                def y_var_ui():
                    df=current_df.get()

                    if df.empty:
                        return ui.input_select(
                            "y_var",
                            "Y variable",
                            choices={"": "No data loaded"},
                            selected=""
                        )

                    plot_type=input.plot_type()

                    if plot_type!="scatter":
                        return ui.div("Y variable is only needed for Scatter Plot.")

                    cols=df.select_dtypes(include="number").columns.tolist()

                    if len(cols) < 2:
                        return ui.input_select(
                            "y_var",
                            "Y variable",
                            choices={"": "Need at least 2 numeric columns"},
                            selected=""
                        )

                    return ui.input_select(
                        "y_var",
                        "Y variable",
                        choices={col: col for col in cols},
                        selected=cols[1]
                    )
        ui.br()

        # Block 3: Plot Output
        with ui.card(class_="content-card"):
            ui.div("Plot Output", class_="status-title")


            @render.plot
            def eda_plot():
                df=current_df.get()
                fig, ax=plt.subplots(figsize=(8, 5))

                if df.empty:
                    ax.text(0.5, 0.5, "No data loaded", ha="center", va="center")
                    ax.axis("off")
                    return fig

                plot_type=input.plot_type()
                x_var=input.x_var()

                try:
                    if plot_type=="scatter":
                        y_var=input.y_var()

                        if x_var not in df.columns or y_var not in df.columns:
                            ax.text(0.5, 0.5, "Please select valid X and Y variables.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        plot_df=df[[x_var, y_var]].dropna()

                        if plot_df.empty:
                            ax.text(0.5, 0.5, "No valid data to plot.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        ax.scatter(plot_df[x_var], plot_df[y_var])
                        ax.set_xlabel(x_var)
                        ax.set_ylabel(y_var)
                        ax.set_title(f"{y_var} vs {x_var}")

                    elif plot_type=="hist":
                        if x_var not in df.columns:
                            ax.text(0.5, 0.5, "Please select a valid variable.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        series=df[x_var].dropna()

                        if series.empty:
                            ax.text(0.5, 0.5, "No valid data to plot.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        ax.hist(series, bins=20)
                        ax.set_xlabel(x_var)
                        ax.set_title(f"Histogram of {x_var}")

                    elif plot_type=="box":
                        if x_var not in df.columns:
                            ax.text(0.5, 0.5, "Please select a valid variable.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        series=df[x_var].dropna()

                        if series.empty:
                            ax.text(0.5, 0.5, "No valid data to plot.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        ax.boxplot(series)
                        ax.set_title(f"Box Plot of {x_var}")
                        ax.set_xticklabels([x_var])

                    elif plot_type=="bar":
                        if x_var not in df.columns:
                            ax.text(0.5, 0.5, "Please select a valid variable.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        counts=df[x_var].astype(str).value_counts(dropna=False).head(10)

                        if counts.empty:
                            ax.text(0.5, 0.5, "No valid data to plot.", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        ax.bar(counts.index, counts.values)
                        ax.set_title(f"Bar Chart of {x_var}")
                        ax.tick_params(axis="x", rotation=45)

                except Exception as e:
                    ax.clear()
                    ax.text(0.5, 0.5, f"Plot error: {e}", ha="center", va="center")
                    ax.axis("off")

                return fig
        ui.br()

        # Block 4: Correlation Controls
        with ui.card(class_="content-card"):
            ui.div("Correlation Analysis", class_="status-title")


            @render.ui
            def corr_vars_ui():
                df=current_df.get()

                if df.empty:
                    return ui.div("No data loaded")

                numeric_cols=df.select_dtypes(include="number").columns.tolist()

                if len(numeric_cols) < 2:
                    return ui.div("Need at least 2 numeric columns for correlation analysis")

                return ui.input_selectize(
                    "corr_vars",
                    "Select numeric variables",
                    choices=numeric_cols,
                    selected=numeric_cols[:4],
                    multiple=True
                )
        ui.br()

        # Block 5: Correlation Output
        with ui.card(class_="content-card"):
            ui.div("Correlation Heatmap", class_="status-title")


            @render.plot
            def correlation_heatmap():
                df=current_df.get()
                fig, ax=plt.subplots(figsize=(8, 6))

                if df.empty:
                    ax.text(0.5, 0.5, "No data loaded", ha="center", va="center")
                    ax.axis("off")
                    return fig

                numeric_df=df.select_dtypes(include="number")

                if numeric_df.empty:
                    ax.text(0.5, 0.5, "No numeric columns available", ha="center", va="center")
                    ax.axis("off")
                    return fig

                selected_vars=input.corr_vars()

                if not selected_vars or len(selected_vars) < 2:
                    ax.text(0.5, 0.5, "Please select at least 2 numeric variables.", ha="center", va="center")
                    ax.axis("off")
                    return fig

                corr_df=numeric_df[list(selected_vars)].dropna()

                if corr_df.empty:
                    ax.text(0.5, 0.5, "No valid data for correlation.", ha="center", va="center")
                    ax.axis("off")
                    return fig

                corr_matrix=corr_df.corr()

                im=ax.imshow(corr_matrix, aspect="auto")

                ax.set_xticks(range(len(corr_matrix.columns)))
                ax.set_yticks(range(len(corr_matrix.columns)))

                ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
                ax.set_yticklabels(corr_matrix.columns)

                ax.set_title("Correlation Heatmap")

                # correlation value
                for i in range(len(corr_matrix)):
                    for j in range(len(corr_matrix)):
                        ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                                ha="center", va="center")

                fig.colorbar(im, ax=ax)

                return fig
        ui.br()

@reactive.effect
@reactive.event(input.data_source, input.sample_dataset)
def _load_sample():
    if input.data_source() != "sample":
        return

    selected_dataset = input.sample_dataset()
    if not selected_dataset:
        current_df.set(pd.DataFrame())
        data_source_info.set({
            "source_type": "sample",
            "source_name": None,
            "status": "idle",
            "message": "Please select a sample dataset."
        })
        return

    try:
        df = load_sample_dataset(selected_dataset)
        current_df.set(df)
        data_source_info.set({
            "source_type": "sample",
            "source_name": selected_dataset,
            "status": "success",
            "message": f"Loaded successfully | {selected_dataset} | {df.shape[0]} rows × {df.shape[1]} columns"
        })
    except Exception as e:
        current_df.set(pd.DataFrame())
        data_source_info.set({
            "source_type": "sample",
            "source_name": selected_dataset,
            "status": "error",
            "message": f"Failed to load sample dataset: {e}"
        })

@reactive.effect
@reactive.event(input.file_upload, input.data_source)
def _load_upload():
    if input.data_source() != "upload":
        return

    files = input.file_upload()
    if not files:
        current_df.set(pd.DataFrame())
        data_source_info.set({
            "source_type": "upload",
            "source_name": None,
            "status": "idle",
            "message": "Please upload a file."
        })
        return

    fileinfo = files[0]
    try:
        df = read_uploaded_file(fileinfo)
        current_df.set(df)
        data_source_info.set({
            "source_type": "upload",
            "source_name": fileinfo["name"],
            "status": "success",
            "message": f"Loaded successfully | {fileinfo['name']} | {df.shape[0]} rows × {df.shape[1]} columns"
        })
    except Exception as e:
        current_df.set(pd.DataFrame())
        data_source_info.set({
            "source_type": "upload",
            "source_name": fileinfo["name"],
            "status": "error",
            "message": f"Upload failed: {e}"
        })

# -----------------------------------------Data preprocessing_Page2-----------------------------------------

    with ui.nav_panel("Page 2"):
        ui.markdown("This is page 2.")

