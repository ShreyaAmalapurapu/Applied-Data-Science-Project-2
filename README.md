# GU5243 Project02
### Collaborators：Haowen Cui(@HowardCui),
## Project Introduction 
(project intro ....)

## Exploratory Data Analysis (EDA)

This section provides a quick overview of the dataset, including key statistics that describe its structure and quality.

Displayed metrics include:

- **Rows** – total number of observations in the dataset  
- **Columns** – total number of variables  
- **Missing Cells** – total number of missing values  
- **Duplicate Rows** – number of duplicated observations  
- **Numeric Columns** – number of numerical variables  
- **Categorical Columns** – number of non-numeric variables  

This summary helps users quickly understand the dataset before performing deeper analysis.

### Visualization Controls

This section allows users to select the type of visualization and the variables used in the plot.

Available plot types include:

- **Scatter Plot**
- **Histogram**
- **Box Plot**
- **Bar Chart**

The available variables update automatically depending on the selected plot type.

#### Plot Type Requirements

- **Scatter Plot**
  - Requires two numeric variables (X and Y).
- **Histogram**
  - Requires one numeric variable.
- **Box Plot**
  - Requires one numeric variable.
- **Bar Chart**
  - Can use any column.

### Correlation Analysis Requirements

- At least **two numeric variables** must be selected.
Users can dynamically choose variables from the dataset.

### How to Use

#### Step 1: Load a Dataset

Navigate to the **Data Upload** page and load data using one of the following methods:

- Select a **sample dataset**
- Upload your own dataset file

Supported file formats:

- `.csv`
- `.xlsx`
- `.json`
- `.rds`

Once the dataset is loaded successfully, the EDA page will display the analysis panels.

---

#### Step 2: Review Dataset Summary

Check the **Dataset Summary** panel to understand:

- dataset size
- number of variables
- missing values
- duplicate rows

This provides a quick overview of the dataset quality.

---

#### Step 3: Choose a Visualization

Go to **Visualization Controls** and select a plot type:

- Scatter Plot
- Histogram
- Box Plot
- Bar Chart

---

#### Step 4: Select Variables

Choose the variables required for the selected plot.

Examples:

- Scatter Plot → choose **X** and **Y** variables  
- Histogram → choose **one numeric variable**  
- Box Plot → choose **one numeric variable**  
- Bar Chart → choose **any column**

---

#### Step 5: Interpret the Plot

Review the generated visualization in the **Plot Output** section.

---

#### Step 6: Explore Correlations

In the **Correlation Analysis** section:

1. Select multiple numeric variables.
2. View the resulting **correlation heatmap**.

