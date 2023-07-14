from fastapi import APIRouter
import numpy as np
import pandas as pd
from models.financial_ratio import FinancialRatio
import utils.database

router = APIRouter()

# select all item
@router.get("")
def get_Financial_ratio():
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = "SELECT * FROM FinancialRatio"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)
        
        if df.empty:
            return {"error": "Financial Ratio not found"}

        return df.to_dict('records')

    except Exception as e:
        return {"message": str(e)}

# select id
@router.get("/{ratio_id}")
def get_financial_ratio_info(ratio_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT * FROM FinancialRatio WHERE RatioID = {ratio_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            
        if row is None:
            return {"error": "Financial Ratio not found"}
        
        if row:
            return {
                "RatioID": row[0],
                "CompanyID": row[1],
                "Year": row[2],
                "CurrentRatio": row[3],
                "DebtEquityRatio": row[4],
                "ProfitMargin": row[5],
                "ReturnOnAssets": row[6]
            }
       
    except Exception as e:
        return {"message": str(e)}

# create
@router.post("/create-ratio")
def create_company(ratio: FinancialRatio):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        df = pd.DataFrame([ratio.dict()])

        # iloc[0] được sử dụng để truy cập vào phần tử đầu tiên trong cột.
        query = "INSERT INTO [FinancialRatio] (CompanyID, Year, CurrentRatio, DebtEquityRatio, ProfitMargin, ReturnOnAssets) VALUES (?, ?, ?, ?, ?, ?)"
        with conn, conn.cursor() as cursor:
            cursor.execute(query, (
                int(df['CompanyID'].iloc[0]),
                int(df['Year'].iloc[0]),
                float(df['CurrentRatio'].iloc[0]),
                float(df['DebtEquityRatio'].iloc[0]),
                float(df['ProfitMargin'].iloc[0]),
                float(df['ReturnOnAssets'].iloc[0])
            ))
            conn.commit()

        return {"message": "Financial Ratio created successfully"}

    except Exception as e:
        conn.rollback()
        return {"message": str(e)}


#endpoint8 Endpoint tính trung bình cộng của các chỉ số tài chính (CurrentRatio, DebtEquityRatio, ProfitMargin, ReturnOnAssets) theo company_id dùng pandas
@router.get("/fr_avg/{company_id}/")
def get_financialratio_avg(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT CurrentRatio, DebtEquityRatio, ProfitMargin, ReturnOnAssets FROM FinancialRatio WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)
        
        if df.empty:
            return {"error": "Financial Ratio not found"}

        avg = df.mean()
        return avg.to_dict()

    except Exception as e:
        return {"message": str(e)}

