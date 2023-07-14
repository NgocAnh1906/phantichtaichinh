from pydantic import BaseModel

class FinancialStatement(BaseModel):
    CompanyID: int
    Year: int
    Revenue: float
    Profit: float
    Assets: float
    Liabilities: float