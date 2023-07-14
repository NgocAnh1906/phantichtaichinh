from fastapi import APIRouter
import numpy as np
import pandas as pd
from models.cash_flow import CashFlow
import utils.database

router = APIRouter()

# select all item
@router.get("")
def get_cash_flow():
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = "SELECT * FROM CashFlow"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

        if df.empty:
            return {"error": "CashFlow not found"}

        return df.to_dict('records')

    except Exception as e:
        return {"message": str(e)}

# select id
@router.get("/{cash_flow_id}")
def get_cash_flow_info(cash_flow_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT * FROM CashFlow WHERE CashFlowID = {cash_flow_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if row is None:
            return {"error": "CashFlow not found"}
        
        return {
            "CompanyID": row[0],
            "Year": row[1],
            "OperatingCashFlow": row[2],
            "InvestingCashFlow": row[3],
            "FinancingCashFlow": row[4],
        }
       
    except Exception as e:
        return {"message": str(e)}

# create
@router.post("/create-cash-flow")
def create_cash_flow(cash_flow: CashFlow):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        df = pd.DataFrame([cash_flow.dict()])

        # iloc[0] được sử dụng để truy cập vào phần tử đầu tiên trong cột.
        query = "INSERT INTO [CashFlow] (CompanyID, Year, OperatingCashFlow, InvestingCashFlow, FinancingCashFlow) VALUES (?, ?, ?, ?, ?)"
        with conn, conn.cursor() as cursor:
            cursor.execute(query, (
                int(df['CompanyID'].iloc[0]),
                int(df['Year'].iloc[0]),
                float(df['OperatingCashFlow'].iloc[0]),
                float(df['InvestingCashFlow'].iloc[0]),
                float(df['FinancingCashFlow'].iloc[0]),
            ))
            conn.commit()
        
        return {"message": "Cash Flow created successfully"}

    except Exception as e:
        conn.rollback()
        return {"message": str(e)}

#endpoint Endpoint tính tổng lưu chuyển tiền mặt (OperatingCashFlow, InvestingCashFlow, FinancingCashFlow) theo company_id. dùng pandas
@router.get("/cashflow_sum/{company_id}")
def get_cashflow_sum(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT OperatingCashFlow, InvestingCashFlow, FinancingCashFlow FROM CashFlow WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)
        
        if df.empty:
            return {"error": "Financial Ratio not found"}

        avg = df.sum()
        return avg.to_dict()

    except Exception as e:
        return {"message": str(e)}

# phân tích dòng tiền
@router.post("/cash-flow")
def analyze_cash_flow(CompanyID: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")
        
        query = f"SELECT OperatingCashFlow, Assets FROM CashFlow JOIN FinancialStatement ON CashFlow.CompanyID = FinancialStatement.CompanyID WHERE CashFlow.CompanyID = {CompanyID}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            column_names = [desc[0] for desc in cursor.description]
            np_array = np.array(rows)
            df = pd.DataFrame(np_array, columns=column_names)

        if df.empty:
            return {"error": "Cash Flow not found"}

        operating_cash_flow_ratio = df["OperatingCashFlow"] / df["Assets"]
        return {"operating_cash_flow_ratio": operating_cash_flow_ratio.tolist()}
      
    except Exception as e:
        return {"message": "An error occurred.", "error": str(e)}