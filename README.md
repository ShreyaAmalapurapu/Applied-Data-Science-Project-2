# GU5243 Project02
### Collaborators：Haowen Cui(@HowardCui), Yaxuan Hu(@yh3881-cloud), Pablo Rocha Gomez (@prochag), Shreya Amalapurapu
## Project Introduction 
(project intro ....)

## Data Upload

This section allows users to either load a built-in sample dataset or upload their own file for future steps.

### Supported Data Sources
The app provides two ways to load data:

1. **Sample datasets**
   - Useful for testing the app quickly without preparing your own file.
   - Included sample datasets:
     - `penguins` (`.csv`)
     - `cars` (`.json`)
     - `College` (`.rds`)

2. **User-uploaded datasets**
   - Users can upload a local dataset file directly through the interface.
   - Supported file formats:
     - `.csv`
     - `.xlsx`
     - `.json`
     - `.rds`

### How to Use

#### Option 1: Load a Sample Dataset
1. Open the **Data Upload** tab.
2. Under **Choose source**, select **Sample dataset**.
3. Choose one dataset from the dropdown list.
4. The app will automatically load the selected dataset and display:
   - load status
   - number of rows and columns
   - data preview
   - column information
   - dataset structure summary

#### Option 2: Upload Your Own Dataset
1. Open the **Data Upload** tab.
2. Under **Choose source**, select **Upload file**.
3. Click the file upload button and choose a dataset from your computer.
4. After upload, the app will automatically read the file and display:
   - upload status
   - file name
   - number of rows and columns
   - preview of the first 10 rows
   - column types
   - missing-value and uniqueness summary

### Validation and Error Handling

The application checks the uploaded file format before loading the data.

- Accepted extensions: `.csv`, `.xlsx`, `.json`, `.rds`
- If the uploaded file format is not supported, the app returns an error message.
- If file reading fails, the app shows an upload failure message instead of crashing.

### Output Panels in the Data Upload Tab

Once a dataset is loaded, the app provides several panels to help users understand the data:

- **Status**  
  Shows whether loading was successful and reports the dataset name and dimensions.

- **Summary**  
  Displays the total number of rows and columns.

- **Preview**  
  Shows the first several rows of the dataset in an interactive table.

- **Columns**  
  Lists each column name and its data type.

- **Structure**  
  Summarizes missing values and the number of unique values for each column.


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

