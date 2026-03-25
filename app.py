from pathlib import Path
import os
import numpy as np
import pandas as pd
import pyreadr
import matplotlib.pyplot as plt
from shiny import reactive
from shiny import ui as ui_core
from shiny.express import input, render, ui


ui.tags.style(
    """
    /* Tableau-inspired: neutral workspace, flat surfaces, blue accent CTAs */
    :root {
      --ts-bg-app: #e9e9e9;
      --ts-bg-panel: #ffffff;
      --ts-bg-rail: #f3f3f3;
      --ts-border: #c9c9c9;
      --ts-border-soft: #e0e0e0;
      --ts-text: #333333;
      --ts-text-muted: #6f6f6f;
      --ts-accent: #2f6ab0;
      --ts-accent-deep: #24578f;
      --ts-orange: #e8762d;
      --ts-radius: 3px;
      --ts-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --columbia-blue: #b9d9eb;
      --columbia-deep: #7fb9d6;
      --columbia-navy: #0f3d5e;
      --card-border: #d4e6f1;
      --text-main: var(--ts-text);
      --text-muted: var(--ts-text-muted);
    }

    body {
      font-family: var(--ts-font);
      -webkit-font-smoothing: antialiased;
      background: var(--ts-bg-app);
      color: var(--ts-text);
      font-size: 14px;
    }

    /* Left tool column flush to viewport (strip Bootstrap container-fluid inset) */
    .navbar ~ .container-fluid {
      padding-left: 0 !important;
      max-width: 100%;
    }

    .navbar {
      background: var(--ts-bg-panel) !important;
      border: none !important;
      border-bottom: 1px solid var(--ts-border) !important;
      border-radius: 0 !important;
      margin-bottom: 0 !important;
      padding-top: 0 !important;
      padding-bottom: 0 !important;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.04);
    }

    .navbar .container-fluid {
      padding-top: 6px;
      padding-bottom: 6px;
    }

    .navbar-brand {
      color: var(--ts-text) !important;
      font-size: 18px !important;
      font-weight: 600 !important;
      letter-spacing: -0.02em;
      padding-right: 1rem !important;
      border-right: 1px solid var(--ts-border-soft);
      margin-right: 0.75rem !important;
    }

    .navbar-brand::after {
      content: "";
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 1px;
      background: var(--ts-orange);
      margin-left: 8px;
      vertical-align: middle;
      opacity: 0.9;
    }

    .nav-tabs {
      border-bottom: none !important;
      gap: 2px;
    }

    .nav-tabs .nav-link {
      font-size: 13px !important;
      font-weight: 500 !important;
      color: var(--ts-text-muted) !important;
      border: none !important;
      border-radius: var(--ts-radius) var(--ts-radius) 0 0 !important;
      padding: 0.45rem 0.65rem !important;
      margin-bottom: 0 !important;
    }

    .nav-tabs .nav-link:hover {
      color: var(--ts-text) !important;
      background: rgba(0, 0, 0, 0.03) !important;
    }

    .nav-tabs .nav-link.active {
      color: var(--ts-accent) !important;
      background: var(--ts-bg-app) !important;
      border: 1px solid var(--ts-border) !important;
      border-bottom-color: var(--ts-bg-app) !important;
      font-weight: 600 !important;
    }

    .card {
      border: 1px solid var(--ts-border-soft) !important;
      border-radius: var(--ts-radius) !important;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06) !important;
      background: var(--ts-bg-panel) !important;
      padding: 10px 12px !important;
    }

    .left-tools.card {
      background: var(--ts-bg-rail) !important;
      border-color: var(--ts-border) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    }

    .section-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--ts-text);
      margin-bottom: 6px;
      letter-spacing: -0.01em;
    }

    .section-subtitle {
      font-size: 13px;
      color: var(--ts-text-muted);
      margin-bottom: 6px;
    }

    .group-title {
      font-size: 12px;
      font-weight: 600;
      color: var(--ts-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-top: 8px;
      margin-bottom: 4px;
    }

    .feature-block {
      background: var(--ts-bg-panel);
      border: 1px solid var(--ts-border-soft);
      border-radius: var(--ts-radius);
      padding: 8px 10px;
      margin-bottom: 8px;
    }

    hr {
      margin-top: 8px !important;
      margin-bottom: 8px !important;
    }

    .mode-switch .form-check {
      display: inline-block;
      margin-right: 10px;
      margin-bottom: 8px;
    }

    .mode-switch .form-check-input {
      display: none;
    }

    .mode-switch .form-check-label {
      border: 1px solid transparent;
      border-radius: var(--ts-radius);
      padding: 5px 10px;
      background: rgba(255, 255, 255, 0.55);
      color: var(--ts-text-muted);
      cursor: pointer;
      font-size: 12px !important;
      font-weight: 500 !important;
    }

    .mode-switch .form-check-input:checked + .form-check-label {
      background: var(--ts-bg-panel);
      border-color: var(--ts-border);
      color: var(--ts-accent);
      font-weight: 600 !important;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
    }

    .mode-content {
      min-height: 0;
      overflow: visible;
      border: none;
      border-radius: 0;
      padding: 8px 0;
      background: transparent;
    }

    .user-guide-page {
      background: var(--ts-bg-panel);
      min-height: 0;
      border: 1px solid var(--ts-border-soft);
      border-radius: var(--ts-radius);
      padding: 16px 20px;
      max-width: 52rem;
      margin: 12px 16px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.07);
    }

    .user-guide-page p,
    .user-guide-page li {
      line-height: 1.85;
    }

    .compact-feedback {
      padding-top: 6px !important;
      padding-bottom: 6px !important;
      min-height: 64px;
    }

    .small-card {
      padding-top: 2px !important;
      padding-bottom: 2px !important;
      min-height: 58px;
    }

    .small-card .section-title,
    .small-empty .section-title {
      margin-bottom: 2px;
      font-size: 16px;
      font-weight: 600;
    }

    .small-card .alert {
      margin-bottom: 0 !important;
      padding-top: 4px;
      padding-bottom: 4px;
      min-height: 24px;
    }

    .small-empty .alert {
      margin-bottom: 0 !important;
      padding-top: 4px;
      padding-bottom: 4px;
      min-height: 24px;
    }

    .small-empty {
      padding-top: 2px !important;
      padding-bottom: 2px !important;
      min-height: 58px;
    }

    .data-preview-card {
      min-height: 0;
    }

    .dense-grid {
      max-height: none;
      overflow: visible;
    }

    .eda-plot-card {
      min-height: 0;
    }

    .eda-plot-card img, .eda-plot-card canvas {
      max-height: 280px !important;
      width: auto !important;
    }

    .left-tools .section-title {
      font-size: 15px !important;
      font-weight: 600 !important;
      margin-bottom: 4px !important;
      color: var(--ts-text) !important;
    }

    .left-tools .group-title {
      font-size: 11px !important;
      font-weight: 600 !important;
      margin-top: 4px !important;
      margin-bottom: 2px !important;
      color: var(--ts-text-muted) !important;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .left-tools .form-label,
    .left-tools .control-label {
      font-size: 12px !important;
      font-weight: 500 !important;
      margin-bottom: 2px !important;
      color: var(--ts-text) !important;
    }

    .left-tools .form-check-label {
      font-size: 12px !important;
      font-weight: 500 !important;
    }

    .left-tools .form-select,
    .left-tools .form-control {
      font-size: 13px !important;
      min-height: 30px !important;
      padding: 4px 8px !important;
      border-radius: var(--ts-radius) !important;
      border-color: #b3b3b3 !important;
    }

    .left-tools .btn,
    .left-tools .btn-default {
      font-size: 12px !important;
      font-weight: 600 !important;
      padding: 5px 12px !important;
      border-radius: var(--ts-radius) !important;
      background: var(--ts-accent) !important;
      border: 1px solid var(--ts-accent-deep) !important;
      color: #fff !important;
    }

    .left-tools .btn:hover,
    .left-tools .btn-default:hover {
      background: var(--ts-accent-deep) !important;
      border-color: #1a4675 !important;
      color: #fff !important;
    }

    .left-tools .shiny-input-container {
      margin-bottom: 5px !important;
    }

    .left-tools .feature-block {
      padding: 5px 7px !important;
      margin-bottom: 4px !important;
    }

    .left-tools .mode-content {
      min-height: 0;
      padding: 5px;
    }

    .eda-viz-panel .section-title {
      margin-bottom: 2px !important;
    }

    .eda-viz-columns {
      margin-bottom: 4px !important;
    }

    .eda-viz-columns > [class*="col-"] {
      min-width: 0;
    }

    .eda-viz-panel .selectize-control {
      max-width: 100% !important;
    }

    .eda-viz-panel .shiny-input-container .irs {
      width: 100% !important;
      max-width: 100% !important;
    }

    .eda-viz-panel .irs {
      margin-top: 2px !important;
      margin-bottom: 2px !important;
    }

    .eda-viz-generate {
      margin-top: 2px !important;
      margin-bottom: 0 !important;
    }

    .eda-viz-generate .shiny-input-container {
      margin-bottom: 0 !important;
    }

    .eda-viz-panel .form-group,
    .eda-viz-panel .mb-3 {
      margin-bottom: 6px !important;
    }

    .eda-viz-panel.card {
      padding-bottom: 8px !important;
    }

    .left-tools .selectize-input {
      min-height: 30px !important;
      padding: 4px 8px !important;
      font-size: 13px !important;
      border-radius: var(--ts-radius) !important;
    }

    .tab-content {
      background: var(--ts-bg-app);
      border: none !important;
      padding-top: 8px !important;
    }

    .tab-pane {
      background: transparent !important;
    }

    input[type="radio"],
    input[type="checkbox"] {
      accent-color: var(--ts-accent);
    }

    .form-label, .control-label {
      font-size: 13px !important;
      font-weight: 500 !important;
      color: var(--ts-text) !important;
      margin-bottom: 4px !important;
    }

    .shiny-input-container {
      margin-bottom: 10px !important;
    }

    .btn, .btn-default {
      font-size: 13px !important;
      font-weight: 500 !important;
      border-radius: var(--ts-radius) !important;
      border: 1px solid #a8a8a8 !important;
      background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%) !important;
      color: var(--ts-text) !important;
      box-shadow: none !important;
    }

    .btn:hover, .btn-default:hover {
      background: linear-gradient(180deg, #f5f5f5 0%, #e5e5e5 100%) !important;
      border-color: #8c8c8c !important;
      color: #000 !important;
    }

    .alert {
      border-radius: var(--ts-radius);
      font-size: 13px;
      font-weight: 500;
      border: 1px solid var(--ts-border-soft);
    }

    .alert-success {
      background: #e8f4ea;
      border-color: #a3c9a8;
      color: #1b5e20;
    }

    .alert-danger {
      background: #fce8e6;
      border-color: #e0a19c;
      color: #8b1a12;
    }

    .alert-secondary {
      background: #f0f0f0;
      border-color: #c9c9c9;
      color: #505050;
    }

    .summary-table, .history-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    .summary-table th, .history-table th {
      text-align: left;
      color: var(--ts-text);
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      border-bottom: 2px solid var(--ts-border);
      padding: 8px 10px;
      background: #fafafa;
    }

    .summary-table td, .history-table td {
      border-bottom: 1px solid var(--ts-border-soft);
      padding: 8px 10px;
    }

    .summary-table td:last-child, .summary-table th:last-child {
      width: 150px;
      text-align: right;
      font-weight: 700;
    }
    """
)

app_dir = Path(__file__).resolve().parent / "sampledatasets"

current_df = reactive.value(pd.DataFrame())
original_df = reactive.value(pd.DataFrame())
operation_log = reactive.value([])

upload_status = reactive.value({"status": "idle", "message": "No data loaded yet."})
cleaning_status = reactive.value({"status": "idle", "message": ""})
fe_status = reactive.value({"status": "idle", "message": ""})
eda_status = reactive.value({"status": "idle", "message": ""})
dropdown_choices = reactive.value({"numeric": [], "all": [], "categorical": []})
engineered_columns = reactive.value([])


def add_log(action: str) -> None:
    operation_log.set(operation_log.get() + [action])


def status_box(info: dict):
    status = info.get("status", "idle")
    if status == "success":
        cls = "alert alert-success"
    elif status == "error":
        cls = "alert alert-danger"
    else:
        cls = "alert alert-secondary"
    return ui.div(info.get("message", ""), class_=cls)


def _read_rds(path: str) -> pd.DataFrame:
    result = pyreadr.read_r(path)
    if not result:
        return pd.DataFrame()
    first_key = next(iter(result.keys()))
    obj = result[first_key]
    return obj if isinstance(obj, pd.DataFrame) else pd.DataFrame(obj)


def read_uploaded_file(fileinfo: dict) -> pd.DataFrame:
    path = fileinfo["datapath"]
    name = fileinfo["name"]
    ext = os.path.splitext(name)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")
    if ext == ".json":
        return pd.read_json(path)
    if ext == ".rds":
        return _read_rds(path)
    if ext == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file format: {ext}")


def load_sample_dataset(name: str) -> pd.DataFrame:
    if name == "penguins":
        return pd.read_csv(app_dir / "penguins.csv")
    if name == "cars":
        return pd.read_json(app_dir / "cars.json")
    if name == "College":
        return _read_rds(str(app_dir / "College.rds"))
    raise ValueError(f"Unknown sample dataset: {name}")


def summary_html(df: pd.DataFrame):
    if df.empty:
        return ui.div("No data loaded", class_="alert alert-secondary")
    rows_data = [
        ("Rows", int(df.shape[0])),
        ("Columns", int(df.shape[1])),
        ("Missing Cells", int(df.isna().sum().sum())),
        ("Duplicate Rows", int(df.duplicated().sum())),
        ("Numeric Columns", int(df.select_dtypes(include="number").shape[1])),
        ("Categorical Columns", int(df.select_dtypes(exclude="number").shape[1])),
    ]
    rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows_data)
    return ui.HTML(
        f"""
        <table class="summary-table">
          <thead><tr><th>Metric</th><th>Value</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        """
    )


with ui.navset_bar(
    title="Data Studio",
    padding=[12, 16, 12, 0],
):
    with ui.nav_panel("User Guide"):
        with ui.div(class_="user-guide-page"):
            ui.div("User Guide", class_="section-title")
            ui.markdown(
                """
                1. **Data Upload**: Load sample data or upload your file.
                2. **Cleaning**: Choose a mode on the left, then apply preprocessing.
                3. **Feature Engineering**: Add or transform columns interactively.
                4. **EDA**: Configure plots and filters, then inspect output.
                5. **Export**: Download the current processed dataset.
                """
            )

    with ui.nav_panel("Data Upload"):
        with ui.layout_columns(col_widths=(4, 8)):
            with ui.card(class_="left-tools"):
                ui.div("Data Upload", class_="section-title")
                with ui.div(class_="feature-block"):
                    ui.div("Upload Dataset", class_="group-title")
                    ui.input_file(
                        "file_upload",
                        "Choose a file",
                        accept=[".csv", ".xlsx", ".json", ".rds", ".parquet"],
                        multiple=False,
                    )
                with ui.div(class_="feature-block"):
                    ui.div("Load Sample Dataset", class_="group-title")
                    ui.input_select(
                        "sample_dataset",
                        "Sample data",
                        choices={"": "Select sample", "penguins": "Penguins", "cars": "Cars", "College": "College"},
                        selected="",
                    )
                    ui.input_action_button("load_sample_btn", "Load selected sample")

            with ui.div():
                with ui.card(class_="compact-feedback"):
                    ui.div("Current Data State", class_="section-title")
                    @render.ui
                    def upload_status_ui():
                        return status_box(upload_status.get())
                with ui.card(class_="data-preview-card"):
                    with ui.layout_columns(col_widths=(4, 8)):
                        with ui.div():
                            ui.div("Summary", class_="group-title")
                            @render.ui
                            def upload_summary_ui():
                                return summary_html(current_df.get())
                        with ui.div(class_="dense-grid"):
                            ui.div("Preview", class_="group-title")
                            @render.data_frame
                            def upload_preview():
                                df = current_df.get()
                                if df.empty:
                                    return render.DataGrid(pd.DataFrame({"Message": ["No data loaded"]}), width="100%", height="220px")
                                return render.DataGrid(df.head(15), width="100%", height="220px")

    with ui.nav_panel("Cleaning"):
        with ui.layout_columns(col_widths=(4, 8)):
            with ui.card(class_="left-tools"):
                ui.div("Cleaning & Preprocessing", class_="section-title")
                ui.input_radio_buttons(
                    "cleaning_mode",
                    None,
                    choices={
                        "missing": "Missing",
                        "dup": "Duplicates",
                        "outlier": "Outliers",
                        "scaling": "Scaling",
                        "encoding": "Encoding",
                        "dtype": "Data Types",
                    },
                    selected="missing",
                    inline=True,
                )
                with ui.div(class_="mode-content"):
                    with ui.panel_conditional("input.cleaning_mode == 'missing'"):
                        ui.input_select(
                            "missing_method",
                            "Method",
                            {
                                "drop_rows": "Drop rows",
                                "drop_cols": "Drop columns",
                                "mean": "Mean imputation",
                                "median": "Median imputation",
                                "mode": "Mode imputation",
                                "constant": "Constant value",
                            },
                            selected="mean",
                        )
                        ui.input_text("constant_value", "Fill value", "0")
                        ui.input_selectize("missing_columns", "Columns (optional)", [], multiple=True)
                        ui.input_action_button("apply_missing", "Apply")

                    with ui.panel_conditional("input.cleaning_mode == 'dup'"):
                        ui.input_action_button("remove_duplicates", "Remove duplicates")

                    with ui.panel_conditional("input.cleaning_mode == 'outlier'"):
                        ui.input_select("outlier_col", "Column", choices={})
                        ui.input_select("outlier_method", "Method", {"iqr": "IQR", "zscore": "Z-score"}, selected="iqr")
                        ui.input_numeric("outlier_threshold", "Threshold", value=1.5, min=0.1, step=0.1)
                        ui.input_action_button("apply_outlier", "Filter outliers")

                    with ui.panel_conditional("input.cleaning_mode == 'scaling'"):
                        ui.input_selectize("scale_cols", "Columns", [], multiple=True)
                        ui.input_select("scale_method", "Method", {"standard": "Standardization", "minmax": "Min-Max"}, selected="standard")
                        ui.input_action_button("apply_scaling", "Apply scaling")

                    with ui.panel_conditional("input.cleaning_mode == 'encoding'"):
                        ui.input_selectize("encode_cols", "Columns", [], multiple=True)
                        ui.input_select("encode_method", "Method", {"onehot": "One-Hot", "label": "Label Encoding"}, selected="onehot")
                        ui.input_action_button("apply_encoding", "Apply encoding")

                    with ui.panel_conditional("input.cleaning_mode == 'dtype'"):
                        ui.input_select("dtype_col", "Column", choices={})
                        ui.input_select("dtype_target", "Target Type", {"numeric": "Numeric", "string": "String", "datetime": "Datetime"}, selected="string")
                        ui.input_action_button("apply_dtype", "Convert")

                ui.input_action_button("reset_data", "Reset data", class_="mt-2")

            with ui.div():
                with ui.layout_columns(col_widths=(6, 6)):
                    with ui.card(class_="small-card"):
                        ui.div("Operation Feedback", class_="section-title")
                        @render.ui
                        def cleaning_feedback_ui():
                            return status_box(cleaning_status.get())
                    with ui.card(class_="small-empty"):
                        ui.div("Operation History", class_="section-title")
                        @render.ui
                        def operation_history_table():
                            logs = operation_log.get()
                            if not logs:
                                return ui.div("No operations yet", class_="alert alert-secondary")
                            rows = "".join(f"<tr><td>{i}</td><td>{msg}</td></tr>" for i, msg in enumerate(logs, start=1))
                            return ui.HTML(
                                f"""
                                <table class="history-table">
                                  <thead><tr><th>Step</th><th>History</th></tr></thead>
                                  <tbody>{rows}</tbody>
                                </table>
                                """
                            )
                with ui.card(class_="dense-grid"):
                    ui.div("Processed Data Preview", class_="section-title")
                    @render.data_frame
                    def cleaning_preview():
                        df = current_df.get()
                        if df.empty:
                            return render.DataGrid(pd.DataFrame({"Message": ["No data loaded"]}), width="100%", height="200px")
                        return render.DataGrid(df.head(8), width="100%", height="200px")

    with ui.nav_panel("Feature Engineering"):
        with ui.layout_columns(col_widths=(4, 8)):
            with ui.card(class_="left-tools"):
                ui.div("Feature Engineering", class_="section-title")
                ui.input_radio_buttons(
                    "fe_mode",
                    None,
                    choices={"expr": "Expression", "transform": "Transform", "dt": "Datetime", "drop": "Drop Cols"},
                    selected="expr",
                    inline=True,
                )
                with ui.div(class_="mode-content"):
                    with ui.panel_conditional("input.fe_mode == 'expr'"):
                        ui.input_text("fe_expr", "Expression", "")
                        ui.input_text("fe_new_col", "New column name", "")
                        ui.input_action_button("apply_expr", "Create feature")

                    with ui.panel_conditional("input.fe_mode == 'transform'"):
                        ui.input_select("fe_column", "Column", choices={})
                        ui.input_select(
                            "fe_transformation",
                            "Method",
                            {
                                "log": "Log",
                                "square": "Square",
                                "sqrt": "Square Root",
                                "abs": "Absolute",
                                "bin": "Binning",
                            },
                            selected="log",
                        )
                        ui.input_slider("fe_bins", "Bins", min=2, max=10, value=4)
                        ui.input_action_button("apply_fe", "Apply transform")

                    with ui.panel_conditional("input.fe_mode == 'dt'"):
                        ui.input_select("datetime_col", "Datetime column", choices={})
                        ui.input_select(
                            "datetime_part",
                            "Extract",
                            {"year": "Year", "month": "Month", "day": "Day", "weekday": "Weekday", "quarter": "Quarter"},
                            selected="year",
                        )
                        ui.input_action_button("apply_datetime_extract", "Extract")

                    with ui.panel_conditional("input.fe_mode == 'drop'"):
                        ui.input_selectize("drop_cols", "Columns to drop", choices=[], multiple=True)
                        ui.input_action_button("apply_drop_cols", "Drop selected columns")

            with ui.div():
                with ui.layout_columns(col_widths=(6, 6)):
                    with ui.card(class_="small-card"):
                        ui.div("Feature Feedback", class_="section-title")
                        @render.ui
                        def feature_feedback_ui():
                            return status_box(fe_status.get())
                    with ui.card(class_="small-empty"):
                        ui.div("Engineered Variables", class_="section-title")
                        @render.ui
                        def engineered_columns_ui():
                            cols = engineered_columns.get()
                            if not cols:
                                return ui.div("No engineered columns yet", class_="alert alert-secondary")
                            rows = "".join(
                                f"<tr><td>{c['name']}</td><td>{c['derived_from']}</td><td>{c['transformation']}</td></tr>"
                                for c in cols
                            )
                            return ui.HTML(
                                f"""
                                <table class="history-table">
                                  <thead><tr><th>New Column</th><th>Derived From</th><th>Method</th></tr></thead>
                                  <tbody>{rows}</tbody>
                                </table>
                                """
                            )
                with ui.card(class_="dense-grid"):
                    ui.div("Current Data Preview", class_="section-title")
                    @render.data_frame
                    def feature_preview():
                        df = current_df.get()
                        if df.empty:
                            return render.DataGrid(pd.DataFrame({"Message": ["No data loaded"]}), width="100%", height="200px")
                        return render.DataGrid(df.head(8), width="100%", height="200px")

    with ui.nav_panel("EDA"):
        with ui.layout_columns(col_widths=(4, 8)):
            with ui.card(class_="left-tools eda-viz-panel"):
                ui.div("Visualization", class_="section-title")
                ui_core.row(
                    ui_core.column(
                        6,
                        ui.div("Plot", class_="group-title"),
                        ui.input_select(
                            "plot_type",
                            "Plot Type",
                            {
                                "hist": "Histogram",
                                "box": "Box Plot",
                                "bar": "Bar Chart",
                                "scatter": "Scatter Plot",
                                "corr": "Correlation Heatmap",
                            },
                            selected="hist",
                        ),
                        ui.input_select("x_var", "X Axis", choices={}),
                        ui.input_select("y_var", "Y Axis", choices={}),
                        ui.input_select("color_var", "Color (optional)", choices={"": "None"}),
                    ),
                    ui_core.column(
                        6,
                        ui.div("Filters", class_="group-title"),
                        ui.input_select("num_filter_col", "Numeric filter", choices={"": "None"}),
                        ui.input_slider("num_filter_range", "Range", min=0.0, max=1.0, value=[0.0, 1.0]),
                        ui.input_select("cat_filter_col", "Category filter", choices={"": "None"}),
                        ui.input_selectize("cat_filter_vals", "Category values", choices=[], multiple=True),
                    ),
                    class_="g-2 eda-viz-columns",
                )
                with ui.div(class_="eda-viz-generate"):
                    ui.input_action_button("generate_plot", "Generate plot")

            with ui.div():
                with ui.card(class_="eda-plot-card"):
                    ui.div("Plot Output", class_="section-title")
                    @render.plot
                    def eda_plot():
                        _ = input.generate_plot()
                        df = current_df.get()
                        fig, ax = plt.subplots(figsize=(6.5, 3.2))
                        if df.empty:
                            ax.text(0.5, 0.5, "No data loaded", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        plot_df = df.copy()
                        n_col = input.num_filter_col()
                        if n_col and n_col in plot_df.columns and pd.api.types.is_numeric_dtype(plot_df[n_col]):
                            rmin, rmax = input.num_filter_range()
                            plot_df = plot_df[(plot_df[n_col] >= rmin) & (plot_df[n_col] <= rmax)]

                        c_col = input.cat_filter_col()
                        c_vals = input.cat_filter_vals() or []
                        if c_col and c_col in plot_df.columns and c_vals:
                            plot_df = plot_df[plot_df[c_col].astype(str).isin(c_vals)]

                        if plot_df.empty:
                            eda_status.set({"status": "error", "message": "No rows available after filters."})
                            ax.text(0.5, 0.5, "No rows available after filters", ha="center", va="center")
                            ax.axis("off")
                            return fig

                        p = input.plot_type()
                        x = input.x_var()
                        y = input.y_var()
                        color = input.color_var()

                        try:
                            if p == "hist":
                                ax.hist(plot_df[x].dropna(), bins=20)
                                ax.set_title(f"Histogram of {x}")
                            elif p == "box":
                                ax.boxplot(plot_df[x].dropna())
                                ax.set_xticklabels([x])
                                ax.set_title(f"Box Plot of {x}")
                            elif p == "bar":
                                counts = plot_df[x].astype(str).value_counts().head(15)
                                ax.bar(counts.index, counts.values)
                                ax.tick_params(axis="x", rotation=45)
                                ax.set_title(f"Bar Chart of {x}")
                            elif p == "scatter":
                                if color and color in plot_df.columns:
                                    for name, g in plot_df.groupby(color):
                                        ax.scatter(g[x], g[y], label=str(name), alpha=0.7)
                                    ax.legend()
                                else:
                                    ax.scatter(plot_df[x], plot_df[y], alpha=0.7)
                                ax.set_xlabel(x)
                                ax.set_ylabel(y)
                                ax.set_title(f"{y} vs {x}")
                            else:
                                num = plot_df.select_dtypes(include="number")
                                corr = num.corr()
                                im = ax.imshow(corr, aspect="auto")
                                ax.set_xticks(range(len(corr.columns)))
                                ax.set_yticks(range(len(corr.columns)))
                                ax.set_xticklabels(corr.columns, rotation=45, ha="right")
                                ax.set_yticklabels(corr.columns)
                                ax.set_title("Correlation Heatmap")
                                fig.colorbar(im, ax=ax)
                            eda_status.set({"status": "success", "message": f"Plot generated with {len(plot_df)} rows after filters."})
                        except Exception as e:
                            eda_status.set({"status": "error", "message": f"Plot generation failed: {e}"})
                            ax.clear()
                            ax.text(0.5, 0.5, f"Plot error: {e}", ha="center", va="center")
                            ax.axis("off")
                        return fig
                with ui.card(class_="compact-feedback"):
                    ui.div("EDA Feedback", class_="section-title")
                    @render.ui
                    def eda_feedback_ui():
                        info = eda_status.get()
                        msg = (info.get("message") or "").strip()
                        if info.get("status", "idle") == "idle" and not msg:
                            info = {**info, "message": "Ready when you generate a plot."}
                        return status_box(info)

    with ui.nav_panel("Export"):
        with ui.layout_columns(col_widths=(3, 9)):
            with ui.card(class_="left-tools"):
                ui.div("Export", class_="section-title")
                @render.download(filename="processed_data.csv")
                def download_processed_data():
                    df = current_df.get()
                    if df.empty:
                        yield "No data available.\n"
                    else:
                        yield df.to_csv(index=False)

            with ui.card(class_="dense-grid"):
                ui.div("Preview", class_="section-title")
                @render.data_frame
                def export_preview():
                    df = current_df.get()
                    if df.empty:
                        return render.DataGrid(pd.DataFrame({"Message": ["No data loaded"]}), width="100%", height="220px")
                    return render.DataGrid(df.head(15), width="100%", height="220px")


def _after_data_loaded(df: pd.DataFrame, source: str) -> None:
    current_df.set(df.copy())
    original_df.set(df.copy())
    operation_log.set([f"Loaded dataset from {source}"])
    engineered_columns.set([])
    cleaning_status.set({"status": "idle", "message": ""})
    fe_status.set({"status": "idle", "message": ""})
    eda_status.set({"status": "idle", "message": ""})
    upload_status.set({"status": "success", "message": f"Loaded {source}: {df.shape[0]} rows x {df.shape[1]} columns."})


@reactive.effect
@reactive.event(input.load_sample_btn)
def _load_sample():
    selected = input.sample_dataset()
    if not selected:
        upload_status.set({"status": "error", "message": "Please select a sample dataset first."})
        return
    try:
        df = load_sample_dataset(selected)
        _after_data_loaded(df, f"sample '{selected}'")
    except Exception as e:
        upload_status.set({"status": "error", "message": f"Failed to load sample: {e}"})


@reactive.effect
@reactive.event(input.file_upload)
def _load_upload():
    files = input.file_upload()
    if not files:
        return
    fileinfo = files[0]
    try:
        df = read_uploaded_file(fileinfo)
        _after_data_loaded(df, f"file '{fileinfo['name']}'")
    except Exception as e:
        upload_status.set({"status": "error", "message": f"Upload failed: {e}"})


@reactive.effect
def _update_dynamic_choices():
    df = current_df.get()
    all_cols = df.columns.tolist() if not df.empty else []
    numeric_cols = df.select_dtypes(include="number").columns.tolist() if not df.empty else []
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist() if not df.empty else []
    dropdown_choices.set({"numeric": numeric_cols, "all": all_cols, "categorical": categorical_cols})

    ui.update_selectize("missing_columns", choices=all_cols, selected=[])
    ui.update_select("outlier_col", choices={c: c for c in numeric_cols})
    ui.update_selectize("scale_cols", choices=numeric_cols, selected=[])
    ui.update_selectize("encode_cols", choices=categorical_cols, selected=[])
    ui.update_select("dtype_col", choices={c: c for c in all_cols})

    ui.update_select("fe_column", choices={c: c for c in numeric_cols})
    ui.update_select("datetime_col", choices={c: c for c in all_cols})
    ui.update_selectize("drop_cols", choices=all_cols, selected=[])

    ui.update_select("x_var", choices={c: c for c in all_cols})
    ui.update_select("y_var", choices={c: c for c in numeric_cols})
    ui.update_select("color_var", choices={"": "None", **{c: c for c in categorical_cols}})
    ui.update_select("num_filter_col", choices={"": "None", **{c: c for c in numeric_cols}})
    ui.update_select("cat_filter_col", choices={"": "None", **{c: c for c in categorical_cols}})

    cat_col = input.cat_filter_col() if hasattr(input, "cat_filter_col") else ""
    if cat_col and cat_col in df.columns:
        values = sorted(df[cat_col].dropna().astype(str).unique().tolist())
        ui.update_selectize("cat_filter_vals", choices=values, selected=[])
    else:
        ui.update_selectize("cat_filter_vals", choices=[], selected=[])

    num_col = input.num_filter_col() if hasattr(input, "num_filter_col") else ""
    if num_col and num_col in df.columns and pd.api.types.is_numeric_dtype(df[num_col]):
        values = df[num_col].dropna()
        if not values.empty:
            low = float(values.min())
            high = float(values.max())
            if low == high:
                high = low + 1.0
            ui.update_slider("num_filter_range", min=low, max=high, value=[low, high])


@reactive.effect
@reactive.event(input.apply_missing)
def _apply_missing():
    df = current_df.get()
    if df.empty:
        return
    new_df = df.copy()
    method = input.missing_method()
    cols = [c for c in (input.missing_columns() or []) if c in new_df.columns] or new_df.columns.tolist()
    try:
        if method == "drop_rows":
            before = len(new_df)
            new_df = new_df.dropna(subset=cols)
            msg = f"Dropped {before - len(new_df)} rows with missing values."
        elif method == "drop_cols":
            before = new_df.shape[1]
            new_df = new_df.dropna(axis=1)
            msg = f"Dropped {before - new_df.shape[1]} columns with missing values."
        elif method in ("mean", "median", "mode"):
            for c in cols:
                if not new_df[c].isna().any():
                    continue
                if method == "mean" and pd.api.types.is_numeric_dtype(new_df[c]):
                    new_df[c] = new_df[c].fillna(new_df[c].mean())
                elif method == "median" and pd.api.types.is_numeric_dtype(new_df[c]):
                    new_df[c] = new_df[c].fillna(new_df[c].median())
                else:
                    m = new_df[c].mode(dropna=True)
                    new_df[c] = new_df[c].fillna(m.iloc[0] if not m.empty else "Unknown")
            msg = f"Applied {method} imputation on selected columns."
        else:
            fill = input.constant_value()
            for c in cols:
                new_df[c] = new_df[c].fillna(fill)
            msg = f"Filled missing values with '{fill}'."
        current_df.set(new_df)
        cleaning_status.set({"status": "success", "message": msg})
        add_log(f"Cleaning - Missing values: {method}")
    except Exception as e:
        cleaning_status.set({"status": "error", "message": f"Missing-value step failed: {e}"})


@reactive.effect
@reactive.event(input.remove_duplicates)
def _remove_duplicates():
    df = current_df.get()
    if df.empty:
        return
    new_df = df.drop_duplicates()
    removed = len(df) - len(new_df)
    current_df.set(new_df)
    cleaning_status.set({"status": "success", "message": f"Removed {removed} duplicate rows."})
    add_log("Cleaning - Removed duplicates")


@reactive.effect
@reactive.event(input.apply_outlier)
def _apply_outliers():
    df = current_df.get()
    if df.empty:
        return
    col = input.outlier_col()
    if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
        cleaning_status.set({"status": "error", "message": "Please select a valid numeric outlier column."})
        return
    method = input.outlier_method()
    th = float(input.outlier_threshold())
    s = df[col]
    try:
        if method == "iqr":
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            low, high = q1 - th * iqr, q3 + th * iqr
            new_df = df[(s >= low) & (s <= high)]
        else:
            std = s.std()
            if std == 0:
                raise ValueError("Column variance is zero.")
            z = (s - s.mean()) / std
            new_df = df[z.abs() <= th]
        removed = len(df) - len(new_df)
        current_df.set(new_df)
        cleaning_status.set({"status": "success", "message": f"Removed {removed} outlier rows using {method.upper()}."})
        add_log(f"Cleaning - Outlier filter: {method} on {col}")
    except Exception as e:
        cleaning_status.set({"status": "error", "message": f"Outlier step failed: {e}"})


@reactive.effect
@reactive.event(input.apply_scaling)
def _apply_scaling():
    df = current_df.get()
    if df.empty:
        return
    cols = [c for c in (input.scale_cols() or []) if c in df.columns]
    if not cols:
        cleaning_status.set({"status": "error", "message": "Select at least one column for scaling."})
        return
    method = input.scale_method()
    new_df = df.copy()
    for c in cols:
        if not pd.api.types.is_numeric_dtype(new_df[c]):
            continue
        if method == "standard":
            std = new_df[c].std()
            if std != 0:
                new_df[c] = (new_df[c] - new_df[c].mean()) / std
        else:
            cmin, cmax = new_df[c].min(), new_df[c].max()
            if cmax != cmin:
                new_df[c] = (new_df[c] - cmin) / (cmax - cmin)
    current_df.set(new_df)
    cleaning_status.set({"status": "success", "message": f"Applied {method} scaling to {len(cols)} columns."})
    add_log(f"Cleaning - Scaling: {method}")


@reactive.effect
@reactive.event(input.apply_encoding)
def _apply_encoding():
    df = current_df.get()
    if df.empty:
        return
    cols = [c for c in (input.encode_cols() or []) if c in df.columns]
    if not cols:
        cleaning_status.set({"status": "error", "message": "Select at least one column for encoding."})
        return
    method = input.encode_method()
    try:
        if method == "onehot":
            new_df = pd.get_dummies(df, columns=cols, drop_first=False)
        else:
            new_df = df.copy()
            for c in cols:
                new_df[c] = new_df[c].astype("category").cat.codes
        current_df.set(new_df)
        cleaning_status.set({"status": "success", "message": f"Applied {method} encoding to {len(cols)} columns."})
        add_log(f"Cleaning - Encoding: {method}")
    except Exception as e:
        cleaning_status.set({"status": "error", "message": f"Encoding failed: {e}"})


@reactive.effect
@reactive.event(input.apply_dtype)
def _apply_dtype():
    df = current_df.get()
    if df.empty:
        return
    col = input.dtype_col()
    if col not in df.columns:
        return
    target = input.dtype_target()
    new_df = df.copy()
    try:
        if target == "numeric":
            new_df[col] = pd.to_numeric(new_df[col], errors="coerce")
        elif target == "datetime":
            new_df[col] = pd.to_datetime(new_df[col], errors="coerce")
        else:
            new_df[col] = new_df[col].astype(str)
        current_df.set(new_df)
        cleaning_status.set({"status": "success", "message": f"Converted '{col}' to {target}."})
        add_log(f"Cleaning - Convert dtype: {col} to {target}")
    except Exception as e:
        cleaning_status.set({"status": "error", "message": f"Dtype conversion failed: {e}"})


@reactive.effect
@reactive.event(input.reset_data)
def _reset_data():
    base = original_df.get()
    if base.empty:
        return
    current_df.set(base.copy())
    engineered_columns.set([])
    cleaning_status.set({"status": "success", "message": "Data reset to original loaded state."})
    add_log("Cleaning - Reset data")


@reactive.effect
@reactive.event(input.apply_expr)
def _apply_expression_feature():
    df = current_df.get()
    if df.empty:
        return
    expr = input.fe_expr().strip()
    new_col = input.fe_new_col().strip()
    if not expr or not new_col:
        fe_status.set({"status": "error", "message": "Please provide both expression and new column name."})
        return
    try:
        new_df = df.copy()
        new_df[new_col] = new_df.eval(expr)
        current_df.set(new_df)
        engineered_columns.set(engineered_columns.get() + [{"name": new_col, "derived_from": "expression", "transformation": expr}])
        fe_status.set({"status": "success", "message": f"Created feature '{new_col}' from expression."})
        add_log(f"Feature - Expression: {new_col} = {expr}")
    except Exception as e:
        fe_status.set({"status": "error", "message": f"Feature expression failed: {e}"})


@reactive.effect
@reactive.event(input.apply_fe)
def _apply_fe_transform():
    df = current_df.get()
    if df.empty:
        return
    col = input.fe_column()
    if col not in df.columns:
        fe_status.set({"status": "error", "message": "Please select a valid column."})
        return
    if not pd.api.types.is_numeric_dtype(df[col]):
        fe_status.set({"status": "error", "message": "Transform requires numeric column."})
        return
    method = input.fe_transformation()
    new_df = df.copy()
    try:
        if method == "log":
            new_col = f"log_{col}"
            new_df[new_col] = np.log1p(np.clip(new_df[col], a_min=0, a_max=None))
        elif method == "square":
            new_col = f"sq_{col}"
            new_df[new_col] = new_df[col] ** 2
        elif method == "sqrt":
            new_col = f"sqrt_{col}"
            new_df[new_col] = np.sqrt(np.clip(new_df[col], a_min=0, a_max=None))
        elif method == "abs":
            new_col = f"abs_{col}"
            new_df[new_col] = new_df[col].abs()
        else:
            new_col = f"bin_{col}"
            new_df[new_col] = pd.cut(new_df[col], bins=input.fe_bins(), labels=False).astype(float)
        current_df.set(new_df)
        engineered_columns.set(engineered_columns.get() + [{"name": new_col, "derived_from": col, "transformation": method}])
        fe_status.set({"status": "success", "message": f"Applied {method}. New column: '{new_col}'."})
        add_log(f"Feature - Transform: {method} on {col}")
    except Exception as e:
        fe_status.set({"status": "error", "message": f"Transform failed: {e}"})


@reactive.effect
@reactive.event(input.apply_datetime_extract)
def _apply_datetime_extract():
    df = current_df.get()
    if df.empty:
        return
    col = input.datetime_col()
    if col not in df.columns:
        return
    part = input.datetime_part()
    try:
        new_df = df.copy()
        dt = pd.to_datetime(new_df[col], errors="coerce")
        mapping = {
            "year": dt.dt.year,
            "month": dt.dt.month,
            "day": dt.dt.day,
            "weekday": dt.dt.weekday,
            "quarter": dt.dt.quarter,
        }
        new_col = f"{col}_{part}"
        new_df[new_col] = mapping[part]
        current_df.set(new_df)
        engineered_columns.set(engineered_columns.get() + [{"name": new_col, "derived_from": col, "transformation": f"datetime_{part}"}])
        fe_status.set({"status": "success", "message": f"Extracted {part} to '{new_col}'."})
        add_log(f"Feature - Datetime extract: {part} from {col}")
    except Exception as e:
        fe_status.set({"status": "error", "message": f"Datetime extraction failed: {e}"})


@reactive.effect
@reactive.event(input.apply_drop_cols)
def _apply_drop_cols():
    df = current_df.get()
    if df.empty:
        return
    drop_cols = [c for c in (input.drop_cols() or []) if c in df.columns]
    if not drop_cols:
        fe_status.set({"status": "error", "message": "Select columns to drop."})
        return
    new_df = df.drop(columns=drop_cols)
    current_df.set(new_df)
    fe_status.set({"status": "success", "message": f"Dropped {len(drop_cols)} columns."})
    add_log(f"Feature - Dropped columns: {', '.join(drop_cols)}")
