from fastapi import APIRouter
import numpy as np
import pandas as pd
from models.company import Company
import utils.database

router = APIRouter()

# endpoint1  select all item


@router.get("")
def get_company():
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = "SELECT * FROM Company"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

        if df.empty:
            return {"error": "Company not found"}

        return df.to_dict('records')

    except Exception as e:
        return {"message": str(e)}


# endpoint1  select id
@router.get("/{company_id}")
def get_company_info(company_id: int):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        query = f"SELECT * FROM Company WHERE CompanyID = {company_id}"
        with conn, conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if row is None:
            return {"error": "Company not found"}

        return {
            "CompanyID": row[0],
            "CompanyName": row[1],
            "Address": row[2],
            "ContactNumber": row[3]
        }

    except Exception as e:
        return {"message": str(e)}


@router.post("/create-company")
def create_company(company: Company):
    try:
        conn = utils.database.create_connection()
        if conn is None:
            raise Exception(f"Unable to connect to the database.")

        df = pd.DataFrame([company.dict()])

        query = "INSERT INTO [Company] (CompanyName, Address, ContactNumber) VALUES (?, ?, ?)"
        with conn, conn.cursor() as cursor:
            cursor.execute(query, df['CompanyName'][0],
                           df['Address'][0],
                           df['ContactNumber'][0]
                           )
            cursor.commit()

        return {"message": "Company created successfully"}

    except Exception as e:
        conn.rollback()
        return {"message": str(e)}
