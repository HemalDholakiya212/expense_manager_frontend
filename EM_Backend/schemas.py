from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserSignup(BaseModel):
    first_name : str  
    last_name: str
    email : str
    password : str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class LoginForUser(BaseModel):
    email : str
    password : str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserExpense(BaseModel):
    expense_amount : float
    expense_category : str
    expense_description: str
    expense_date: str
    user_id: int
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserBudget(BaseModel):
    user_id: int
    budget_amount : float
    budget_category : str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class FetchExpenseData(BaseModel):
    user_id: int
    selected_year: int
    selected_month: Optional[int] 
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UploadReceipt(BaseModel):
    user_id: int
    receipt: str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CompareMonths(BaseModel):
    user_id: int
    year:int
    month1:int
    month2:int
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PredictExpense(BaseModel):
    user_id: int
    current_month: int
    current_year: int
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True