from fastapi import FastAPI

from company import endpoints as company_endpoints
from financial_ratio import endpoints as financial_ratio_endpoints
from financial_statement import endpoints as financial_statement_endpoints
from cash_flow import endpoints as cash_flow_endpoints

app = FastAPI()

app.include_router(company_endpoints.router, prefix="/company", tags=["Company"])
app.include_router(financial_ratio_endpoints.router, prefix="/financial-ratio", tags=["Financial Ratio"])
app.include_router(financial_statement_endpoints.router, prefix="/financial-statement", tags=["Financial Statement"])
app.include_router(cash_flow_endpoints.router, prefix="/cash-flow", tags=["Cash Flow"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)