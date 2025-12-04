# Vendor Performance Analysis

## Project Overview

**Vendor Performance Analysis** is an end-to-end data analysis project focused on providing comprehensive insights into vendor operations using data from purchases, sales, invoices, and freight. The goal is to generate vendor-wise sales and purchase summaries, optimize performance handling for large datasets, and support efficient dashboarding and reporting.

Repository: [rajivaleaakash/Vendor-Performance-Analysis](https://github.com/rajivaleaakash/Vendor-Performance-Analysis)  
Main Language: Jupyter Notebook

---

## Key Features

- **Data Ingestion:** Connects to a database and extracts relevant tables for vendor analysis.
- **Data Cleaning:** Standardizes datatype, fills missing values, strips extra spaces from categorical data, and engineers new columns (e.g., Gross Profit, Profit Margin).
- **Vendor Summary Creation:** Merges purchase, sales, invoice, and freight tables to produce a detailed summary per vendor and brand.
- **Performance Optimization:** Employs pre-aggregation to speed up analysis and reporting, manages large-scale joins and aggregations.
- **Advanced Metrics:** Calculates total sales, total purchases, gross profit, and profit margins by vendor and brand.
- **Extensive Reporting:** Facilitates future dashboarding and analytical reporting by storing enriched vendor summaries.

---

## Data Model

| VendorNumber | VendorName              | Brand | Description | PurchasePrice | Volume | TotalPurchaseQuantity | TotalPurchaseDollars | TotalSalesQuantity | TotalSalesDollars | GrossProfit | ProfitMargin (%) | FreightCost | ... |
|--------------|------------------------|-------|-------------|---------------|--------|----------------------|----------------------|-------------------|-------------------|-------------|------------------|-------------|-----|
| (examples)   | (see ipynb tables)     | ...   | ...         | ...           | ...    | ...                  | ...                  | ...               | ...               | ...         | ...              | ...         |     |

---

## Usage

### 1. Exploratory Data Analysis
- Run the notebook `Exploratory_Data_Analysis.ipynb` to explore vendor invoices, sales data, purchase price tables, and perform initial joins.
- Clean and enrich datasets:  
  - Strip whitespace from vendor names  
  - Fill missing values with `0`
- Generate and store summary tables using SQL queries and pandas.

### 2. Vendor Summary Pipeline
- The primary pipeline script is `get_vendor_summary.py`.
- Main functions:
    - `create_vendor_summary(conn)`: Executes SQL to join freight, purchase, and sales summaries by vendor and brand. Adds columns for optimization (gross profit, margin, etc.).
    - `clean_data(df)`: Cleans input dataframe, standardizes types, and engineers features for analysis.
    - Results are loaded to the `vendor_sales_summary` table in your database for future fast queries.

#### Example Pipeline Execution (Python):
```python
from get_vendor_summary import main
main()  # Runs full end-to-end vendor summary pipeline
```

---

## Example Insights

- **Performance Optimization:** Pre-aggregated vendor summaries help avoid repeated expensive computations, essential for analytical dashboards.
- **Vendor Sales Summary:** Quickly analyze metrics like total sales/purchases, margins, and freight costs for all vendors.
- **Dataframe Size:** After aggregation, the summary often contains thousands of rows and more than a dozen data features.

---

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/rajivaleaakash/Vendor-Performance-Analysis.git
    cd Vendor-Performance-Analysis
    ```
2. **Install required packages**
    ```bash
    pip install pandas numpy sqlalchemy jupyter
    ```
3. **Database Configuration**
    - Ensure access to your data tables: `vendor_invoice`, `purchases`, `purchase_prices`, `sales`.
    - Set up connection parameters in `data_ingestion.py`.

4. **Run the Analysis Notebook**
    - Launch:
      ```bash
      jupyter notebook Exploratory_Data_Analysis.ipynb
      ```

5. **Run the Pipeline Script**
    - Execute:
      ```bash
      python get_vendor_summary.py
      ```

---

## Outputs & Reporting

- All enriched data is stored in a target table, e.g. `vendor_sales_summary`, for downstream visualizations and reporting.
- Example insights are visible throughout the Jupyter notebook, with pivot tables and visual metrics.

---

## Author

- [rajivaleaakash](https://github.com/rajivaleaakash)

---

## License

*No license specified*

---