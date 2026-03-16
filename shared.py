from shiny import reactive
import pandas as pd

current_df = reactive.value(pd.DataFrame())

data_source_info = reactive.value({
    "source_type": None,
    "source_name": None
})