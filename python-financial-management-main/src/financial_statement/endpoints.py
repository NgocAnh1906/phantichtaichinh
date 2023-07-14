from fastapi import APIRouter
import numpy as np
import pandas as pd
from models.financial_statement import FinancialStatement
import utils.database
from typing import Union
router = APIRouter()

# select all item
@router.get("")
def get_financial_statement():
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = "SELECT * FROM FinancialStatement"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

        if rows is None:
            return {"error": "Financial Statement not found"}
        
        return df.to_dict('records')

    except Exception as e:
        return {"message": str(e)}

# select id
@router.get("/{statement_id}")
def get_financial_statament_info(statement_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT * FROM FinancialStatement WHERE StatementID = {statement_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if row is None:
            return {"error": "Financial Statement not found"}
        
        return {
            "StatementID": row[0],
            "CompanyID": row[1],
            "Year": row[2],
            "Revenue": row[3],
            "Profit": row[4],
            "Assets": row[5],
            "Liabilities": row[6]
        }

    except Exception as e:
        return {"message": str(e)}

# create
@router.post("/create-statement")
def create_financial_statement(statement: FinancialStatement):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        df = pd.DataFrame([statement.dict()])

        # iloc[0] được sử dụng để truy cập vào phần tử đầu tiên trong cột.
        query = "INSERT INTO [FinancialStatement] (CompanyID, Year, Revenue, Profit, Assets, Liabilities) VALUES (?, ?, ?, ?, ?, ?)"
        with conn, conn.cursor() as cursor:
            cursor.execute(query, (
                int(df['CompanyID'].iloc[0]),
                int(df['Year'].iloc[0]),
                float(df['Revenue'].iloc[0]),
                float(df['Profit'].iloc[0]),
                float(df['Assets'].iloc[0]),
                float(df['Liabilities'].iloc[0])
            ))
            conn.commit()

        return {"message": "Financial Statement created successfully"}

    except Exception as e:
        conn.rollback()
        return {"message": str(e)}

# endpoint: Tính trung bình cộng của Revenue, Profit, Assets ,Liabilities theo company_id dùng numpy
@router.get("/avg/{company_id}")
def get_avg(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Revenue, Profit, Profit, Assets, Liabilities FROM FinancialStatement WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        if rows is None:
            return {"error": "Company not found"}
        
        # Chuyển kết quả thành mảng numpy
        revenue_array = np.array([row[0] for row in rows])
        profit_array = np.array([row[1] for row in rows])
        assets_array = np.array([row[2] for row in rows])
        liabilities_array = np.array([row[3] for row in rows])

        # Tính trung bình cộng của Revenue, Profit, Assets ,Liabilities
        revenue_avg = np.mean(revenue_array)
        profit_avg = np.mean(profit_array)
        assets_avg = np.mean(assets_array)
        liabilities_avg = np.mean(liabilities_array)

        # Trả về trung bình cộng
        return {
            "revenue_avg": float(revenue_avg),
            "profit_avg": float(profit_avg),
            "assets_avg": float(assets_avg),
            "liabilities_avg": float(liabilities_avg)
        }

    except Exception as e:
        return {"message": str(e)}

# endpoint: Tính tỷ lệ lợi nhuận (Profit) trên doanh thu (Revenue) theo company_id dùng numpy


@router.get("/profit_revenue/{company_id}")
def get_profit_revenue(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Revenue, Profit FROM FinancialStatement WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        if rows is None:
            return {"error": "Company not found"}
        
        # Chuyển kết quả thành mảng numpy
        revenue_array = np.array([row[0] for row in rows])
        profit_array = np.array([row[1] for row in rows])

        # Tính tỷ lệ lợi nhuận
        profit_revenue = profit_array / revenue_array

        # Trả về tỷ lệ lợi nhuận
        return {"profit_revenue": profit_revenue.tolist()}

    except Exception as e:
        return {"message": str(e)}

# endpoint trả về độ lệch chuẩn của Revenue, Profit, Assets ,Liabilities theo companyid dùng numpy
@router.get("/fs_std/{company_id}/")
def get_fs_std(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Revenue, Profit, Profit, Assets, Liabilities FROM FinancialStatement WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        if rows is None:
            return {"error": "Company not found"}
        
        # Chuyển kết quả thành mảng numpy
        revenue_array = np.array([row[0] for row in rows])
        profit_array = np.array([row[1] for row in rows])
        assets_array = np.array([row[2] for row in rows])
        liabilities_array = np.array([row[3] for row in rows])

        # Tính độ lệch chuẩn của Profit Revenue, Profit, Assets ,Liabilities
        revenue_std = np.std(revenue_array)
        profit_std = np.std(profit_array)
        assets_std = np.std(assets_array)
        liabilities_std = np.std(liabilities_array)
        # Trả về độ lệch chuẩn của profit
        return {
            "revenue_std": float(revenue_std),
            "profit_std": float(profit_std),
            "assets_std": float(assets_std),
            "liabilities_std": float(liabilities_std)
        }

    except Exception as e:
        return {"message": str(e)}

# endpoint thống kê tổng Profit Revenue, Profit, Assets ,Liabilities theo companyid dùng numpy
@router.get("/fs_sum/{company_id}")
def get_fs_sum(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Revenue, Profit, Profit, Assets, Liabilities FROM FinancialStatement WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        if rows is None:
            return {"error": "Company not found"}
        
        # Chuyển kết quả thành mảng numpy
        revenue_array = np.array([row[0] for row in rows])
        profit_array = np.array([row[1] for row in rows])
        assets_array = np.array([row[2] for row in rows])
        liabilities_array = np.array([row[3] for row in rows])
        # Tính  tổng của Profit Revenue, Profit, Assets ,Liabilities
        revenue_sum = np.sum(revenue_array)
        profit_sum = np.sum(profit_array)
        assets_sum = np.sum(assets_array)
        liabilities_sum = np.sum(liabilities_array)
        # Trả về kết quả
        return {
            "revenue_sum": float(revenue_sum),
            "profit_sum": float(profit_sum),
            "assets_sum": float(assets_sum),
            "liabilities_sum": float(liabilities_sum)
        }


    except Exception as e:
        return {"message": str(e)}

# endpoint Tính tỷ lệ tăng trưởng Revenue và Profit theo company_id sử dụng pandas
@router.get("/revenue_profit_growth/{company_id}")
def get_revenue_profit_growth(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Year, Revenue, Profit FROM FinancialStatement WHERE CompanyID = {company_id} ORDER BY Year ASC"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

        if df.empty:
            return {"error": "Financial Ratio not found"}

        # Tính tỷ lệ tăng trưởng của Revenue và Profit
        revenue_growth = df["Revenue"].pct_change().fillna(0)
        profit_growth = df["Profit"].pct_change().fillna(0)
        # Trả về kết quả
        return {
            "revenue_growth": revenue_growth.tolist(),
            "profit_growth": profit_growth.tolist()
        }
    except Exception as e:
        return {"message": str(e)}


# endpoint Trả về công ty có tỷ lệ lợi nhuận (Profit Ratio) > threshold sử dụng pandas
@router.get("/companies/profit_ratio_threshold")
def get_companies_above_profit_ratio(threshold: Union[float, None] = None):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT CompanyID,Year, Profit, Revenue FROM FinancialStatement"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

        if df.empty:
            return {"error": "No data available"}

        # Tính tỷ lệ lợi nhuận
        df["Profit_Ratio"] = df["Profit"] / df["Revenue"]
        # nếu có input thì trả công ty có tỷ lê lợi nhuận > threshold
        if threshold is not None:
            # Lọc các công ty có tỷ lệ lợi nhuận > threshold
            companies_above_threshold = df[df["Profit_Ratio"] > threshold]
            result_df = companies_above_threshold[["CompanyID", "Year", "Profit_Ratio"]]
        # nếu không có threshold thì trả ra tất cả công ty
        else:
            # Lấy tất cả thông tin công ty
            result_df = df[["CompanyID", "Year", "Profit_Ratio"]]

        # Chuyển kết quả thành dạng dict
        result_dict = result_df.to_dict(orient="records")

        # Trả về kết quả
        return {"companies": result_dict}
    except Exception as e:
        return {"message": str(e)}

# Dự báo tài chính:
@router.post("/forecast")
def forecast_financial_data(companyID: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Year, Revenue FROM FinancialStatement WHERE CompanyID = {companyID}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(rows)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Financial Statement not found"}

        years = df["Year"].unique()
        last_year = years.max()
        next_year = last_year + 1
        last_year_revenue = df.loc[df["Year"] == last_year, "Revenue"].values[0]
        revenue_forecast = np.random.normal(last_year_revenue * 1.05, 100000)

        # Trả về kết quả dưới dạng JSON
        return {"next_year": next_year, "revenue_forecast": revenue_forecast}

    except Exception as e:
        return {"message": str(e)}
    
# Phân tích xu hướng tài chính theo thời gian:
@router.post("/trend")
def analyze_financial_trends(CompanyID: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT * FROM FinancialStatement WHERE CompanyID = {CompanyID}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(rows)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Financial Statement not found"}
        
        revenue_trends = df.groupby("Year")["Revenue"].mean()
        return {"revenue_trends": revenue_trends.to_dict()}

    except Exception as e:
        return {"message": str(e)}
    
# Tính toán tỷ lệ tài chính:
@router.post("/calculate-financial_ratio")
def calculate_financial_ratio(companyID: int, year: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT Profit, Revenue FROM FinancialStatement WHERE CompanyID = {companyID} AND Year = {year}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(rows)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Financial Statement not found"}
        
        profit_margin = (df["Profit"] / df["Revenue"]) * 100
        return {"profit_margin": profit_margin.tolist()}

    except Exception as e:
        return {"message": str(e)}
    
# tính toán lợi nhuận
@router.post("/calculate-profitability")
def calculate_profitability(CompanyID: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")
        
        query = f"SELECT * FROM FinancialStatement WHERE CompanyID = {CompanyID}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            financial_data = cursor.fetchall()
            
            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(financial_data)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Financial Statement not found"}
        
        roa = df["Profit"] / df["Assets"]
        return {"roa": roa.tolist()}
    
    except Exception as e:
        return {"message": "An error occurred.", "error": str(e)}
    

# doanh thu hàng tồn kho
@router.post("/inventory-turnover")
def calculate_inventory_turnover(CompanyID: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception("Unable to connect to the database.")
        
        query = f"SELECT * FROM FinancialStatement WHERE CompanyID = {CompanyID}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(rows)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Financial Statement not found"}
        
        cost_of_goods_sold = df['Profit'].astype(float)  # Assuming Profit represents cost of goods sold
        average_inventory = df['Assets'].astype(float)  # Assuming Assets represents average inventory

        inventory_turnover = cost_of_goods_sold / average_inventory
        return {"inventory_turnover": inventory_turnover}

    except Exception as e:
        return {"message": "An error occurred.", "error": str(e)}

# hoàn lại vốn đầu tư
@router.post("/return-on-investment")
def calculate_return_on_investment(CompanyID: int, investment: float):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception("Unable to connect to the database.")

        query = f"SELECT Profit FROM FinancialStatement WHERE CompanyID = {CompanyID}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(rows)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Financial Statement not found"}
        
        df["ROI"] = (df["Profit"] / investment) * 100
        return {"roi": df["ROI"].tolist()}


    except Exception as e:
        return {"message": "An error occurred.", "error": str(e)}