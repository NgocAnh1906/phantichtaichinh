from pydantic import BaseModel

class CashFlow(BaseModel):
    CompanyID: int
    Year: int
    OperatingCashFlow: float
    InvestingCashFlow: float
    FinancingCashFlow: float