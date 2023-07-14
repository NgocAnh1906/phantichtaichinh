from pydantic import BaseModel

class FinancialRatio(BaseModel):
    CompanyID: int
    Year: int
    CurrentRatio: float
    DebtEquityRatio: float
    ProfitMargin: float
    ReturnOnAssets: float