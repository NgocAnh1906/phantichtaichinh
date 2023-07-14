from pydantic import BaseModel

class Company(BaseModel):
    CompanyName: str
    Address: str
    ContactNumber: str
 
