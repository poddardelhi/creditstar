from dataclasses import dataclass,asdict
from datetime import date, datetime, timedelta
from typing import List, Tuple,Dict,Optional
from pydantic import BaseModel

@dataclass
class User:
    loan_application_product_name: str
    loan_application_sum:int
    loan_application_timestamp:datetime
    loan_application_duration_in_days: int
    loan_application_is_top_up:bool
    loan_applicant_fullname:str
    loan_applicant_birthdate:str
    loan_applicant_is_repeat_client:bool
    UW_decision: str
    notification:str
    dti_ratio:float
    audit_trail: str
    loan_applicant_credit_score: Optional[float]= None
    loan_applicant_income:Optional[float]= None
    loan_applicant_liabilities:Optional[float]= None
    loan_applicant_outstanding_debt_in_debt_registry:Optional[float]= None
    
    
    def __init__(self):
        self.loan_application_product_name=input("loan_application_product_name:")
        self.loan_application_sum=input("loan_application_sum:")
        self.loan_application_timestamp=input("loan_application_timestamp:")
        self.loan_application_duration_in_days=input("loan_application_duration_in_days:") 
        self.loan_application_is_top_up=input("loan_application_is_top_up:")
        self.loan_applicant_fullname=input("loan_applicant_fullname:")
        self.loan_applicant_birthdate=input("loan_applicant_birthdate:")
        self.loan_applicant_credit_score=input("loan_applicant_credit_score:")
        self.loan_applicant_income=input("loan_applicant_income:")
        self.loan_applicant_liabilities=input("loan_applicant_liabilities")
        self.loan_applicant_outstanding_debt_in_debt_registry=input("loan_applicant_outstanding_debt_in_debt_registry")
        self.loan_applicant_is_repeat_client=bool(input("loan_applicant_is_repeat_client:"))      

    def calculate_age(born):
        today=date.today()
        return (today.year-born.year )//timedelta(days=365.2425)

    def application_checker(self):
        age=self.calculate_age(self.loan_applicant_birthdate)
        if (age<=18):
            self.UW_decision="Decline"
        elif(age>80):
            self.notification="Review birthdate and documents of Applicant"
        
        else:
            if(self.loan_application_product_name=='spl17' and self.loan_applicant_credit_score<0):
                self.UW_decision="Decline"
            elif(self.loan_application_product_name=='spl17' and self.loan_applicant_is_repeat_client== True):
                if(self.loan_applicant_credit_score in range(0,10) and self.loan_application_sum<300 ):
                    self.UW_decision="Accept"
                else:
                    self.notification="Review Credit History Manually"
                    self.UW_decision= "Review"
            elif(self.loan_application_product_name=='spl17' and self.loan_applicant_is_repeat_client== False):
                if(self.loan_applicant_credit_score in range(0,5)):
                    if(self.loan_applicant_outstanding_debt_in_debt_registry==0):
                        self.UW_decision="Accept"
                    elif(self.loan_applicant_outstanding_debt_in_debt_registry>0 and self.loan_applicant_outstanding_debt_in_debt_registry<50):
                        self.UW_decision="Review"
                        self.notification="Review Bank Statement"
                    else:self.UW_decision="Decline"
                else: self.UW_decision="Decline"
            elif(self.loan_application_product_name=='top_up'):
                if(age>80):
                    self.notification="Review birthdate and documents of Applicant"
                else:
                    if(self.loan_applicant_credit_score in range( 0,20)):
                        self.UW_decision="Accept"
                    else:
                        self.UW_decision="Decline"
            else:
                if(self.loan_applicant_credit_score in range(0,5)):
                    if(self.loan_applicant_outstanding_debt_in_debt_registry==0):
                        self.UW_decision="Accept"
                    else:
                        if(self.loan_applicant_outstanding_debt_in_debt_registry>0 and self.loan_applicant_outstanding_debt_in_debt_registry<50):
                            self.notification="Review Bank Statement"
                            self.UW_decision="Review"
                        else:
                            self.UW_decision="Decline"

                else:
                    self.UW_decision="Decline"

user_1= User()