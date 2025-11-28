import pandas as pd
import numpy as np
from data_ingestion import create_connection, ingestion_DB
import warnings
warnings.filterwarnings('ignore')
from logging_setup import setup_logger
logger = setup_logger('get_vendor_summary')


def create_vendor_summary(conn):
    """This function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data"""
    try:
        logger.info("Starting vendor summary creation.")
        query = """
                WITH FreightSummary As (
                    SELECT 
                    VendorNumber,
                    SUM(Freight) AS FreightCost
                    FROM vendor_invoice
                    GROUP BY VendorNumber
                ),
                PurchaseSummary AS (
                    SELECT 
                    p.VendorNumber,
                    p.VendorName,
                    p.Brand,
                    p.Description,
                    p.PurchasePrice,
                    pp.Volume,
                    SUM(p.Quantity) AS TotalPurchaseQuantity,
                    SUM(p.Dollars) AS TotalPurchaseDollars
                    FROM purchases p 
                    JOIN purchase_prices pp 
                    ON p.Brand = pp.Brand
                    WHERE p.PurchasePrice > 0
                    GROUP BY p.VendorNumber, p.VendorName, p.Brand,p.Description,p.PurchasePrice,pp.Price,pp.Volume
                ),
                SalesSummary AS (
                    SELECT 
                    VendorNo,
                    Brand,
                    SUM(SalesQuantity) AS TotalSalesQuantity,
                    SUM(SalesDollars) AS TotalSalesDollars,
                    SUM(SalesPrice) AS TotalSalesPrice,
                    SUM(ExciseTax) AS TotalExciseTax
                    FROM sales
                    GROUP BY VendorNo, Brand
                )

                SELECT 
                ps.VendorNumber,
                ps.VendorName,
                ps.Brand,
                ps.Description,
                ps.PurchasePrice,
                ps.Volume,
                ps.TotalPurchaseQuantity,
                ps.TotalPurchaseDollars,
                ss.TotalSalesQuantity,
                ss.TotalSalesDollars,
                ss.TotalSalesPrice,
                ss.TotalExciseTax,
                fs.FreightCost
                FROM PurchaseSummary ps 
                LEFT JOIN SalesSummary ss 
                ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
                LEFT JOIN FreightSummary fs 
                ON fs.VendorNumber = ps.VendorNumber
                ORDER BY ps.TotalPurchaseDollars DESC
            """
        df = pd.read_sql_query(query, conn)
        logger.info(f"Vendor summary created successfully. Rows fetched: {df.shape[0]}")
        return df
    except Exception as e:
        logger.error(f"Failed to create vendor summary: {e}")
        raise

def clean_data(df):
    "This function clean the dataframe and add new features"
    try:
        logger.info("Starting data cleaning process.")

        if df.empty:
            logger.warning("Input dataframe is empty. Cleaning skipped.")
            return df
        # change datatype to float
        df['Volume'] = df['Volume'].astype('float64')

        # Filling missing values with 0
        df.fillna(0, inplace=True)

        # Remove space from categorical columns
        df['VendorName'] = df['VendorName'].str.strip()
        df['Description'] = df['Description'].str.strip()

        # Creating new columns for better analysis
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        df['ProfitMargin'] = np.where(df['TotalSalesDollars'] != 0, (df['GrossProfit'] / df['TotalSalesDollars']) * 100, 0)
        df['StockTurnover'] = np.where(df['TotalPurchaseQuantity'] != 0, df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'], 0)
        df['SalestoPurchaseRatio'] = np.where(df['TotalPurchaseDollars'] != 0,df['TotalSalesDollars'] / df['TotalPurchaseDollars'],0)
        
        logger.info("Data cleaning completed successfully.")
        return df

    except Exception as e:
        logger.error(f"Error occurred during data cleaning: {e}")
        raise

def main():
    try:
        logger.info("vendor summary pipline started.")
        engine = create_connection()
        summary_df = create_vendor_summary(engine)
        clean_summary = clean_data(summary_df)
        status = ingestion_DB(clean_summary, 'vendor_sales_summary',engine)

        if status:
            logger.info("vendor summary pipline completed successfully.")
        else:
            logger.error("vendor summary pipline compeleted with errors during ingestion.")

    except Exception as e:
        logger.error(f"vendor summary pipline execution faild: {e}")
        raise

    
if __name__ == "__main__":
    main()
    