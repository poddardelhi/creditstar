from dataclasses import dataclass, asdict, field
from datetime import date, datetime, timedelta
from typing import List, Tuple, Dict, Optional

@dataclass
class UserOutput:
    UW_decision: str = ''
    notification: List[str] = field(default_factory=list)
    dti_ratio: float = 0.0
    audit_trail: dict = field(default_factory=dict)

@dataclass
class User:
    loan_application_product_name: str
    loan_application_sum: int
    loan_application_timestamp: datetime
    loan_application_duration_in_days: int
    loan_application_is_top_up: bool
    loan_applicant_fullname: str
    loan_applicant_birthdate: str
    loan_applicant_is_repeat_client: bool
    loan_applicant_credit_score: Optional[float] = None
    loan_applicant_income: Optional[float] = None
    loan_applicant_liabilities: Optional[float] = None
    loan_applicant_outstanding_debt_in_debt_registry: Optional[float] = None

    def calculate_age(self, born):
        today = date.today()
        dt = datetime.strptime(self.loan_applicant_birthdate, '%Y-%m-%d')
        return today.year-dt.year - ((today.month, today.day) < (dt.month, dt.day))

    def add_audit_trail(self, result, key, value, description, status=None):
        """Generates the audit trail based on the parameters

        Args:
            result (UserOutput): The result object for the current input
            key (string): Unique value to add in audit trail
            value (string): The value for the key
            description (string): additional information
            status (string): status of the input
        """
        result.audit_trail[key] = {"value": value,
                       "desc": description, "ts": datetime.now()}
        result.audit_trail['status'] = status


    def application_checker(self):
        result = UserOutput()
        dob = self.loan_applicant_birthdate
        age = self.calculate_age(dob)
        if (age < 18):
            self.add_audit_trail(result, "age", age,
                                 "Age below 18 years", "Decline")
            result.UW_decision = "Decline"
        elif(age > 80):
            self.add_audit_trail(result, "age", age,
                                 "Age above 80 years", "Review")
            result.notification.append(
                "Review birthdate and documents of Applicant")
            result.UW_decision = "Review"
        else:
            if(self.loan_application_product_name == 'spl17'):
                self.add_audit_trail(result, "spl17", True, "Product is spl17")

                if (self.loan_applicant_credit_score < 0):
                    self.add_audit_trail(
                        result, "creditScore", self.loan_applicant_credit_score, "Credit score below 0", "Decline")
                    result.UW_decision = "Decline"

                elif(self.loan_applicant_is_repeat_client == True):
                    self.add_audit_trail(
                        result, "repeatClient", True, 'Is a repeat client')

                    if(self.loan_applicant_credit_score <= 10):
                        self.add_audit_trail(result, "creditScore", self.loan_applicant_credit_score,
                                             "Credit score below or equal 10")
                        if (self.loan_application_sum < 300):
                            self.add_audit_trail(result, 'loanApplSum', self.loan_application_sum,
                                                 'loan application sum is less than 300', 'Accept')
                            result.UW_decision = "Accept"

                        else:
                            self.add_audit_trail(result, 'loanApplSum', self.loan_application_sum,
                                                 'loan application sum is greater or equal to 300', 'Review')
                            result.notification.append(
                                'Review Credit History Manually')
                            result.UW_decision = "Review"
                    else:
                        self.add_audit_trail(result, 'creditScore', self.loan_applicant_credit_score,
                                             'Credit score greater than 10', 'Decline')
                        self.UW_decision = "Decline"

                else:
                    self.add_audit_trail(
                        result, "repeatClient", False, 'Is not a repeat client')

                    if(self.loan_applicant_credit_score <= 5):
                        self.add_audit_trail(result, "creditScore", self.loan_applicant_credit_score,
                                             "Credit score below or equal 5")

                        # none type handle
                        if(self.loan_applicant_outstanding_debt_in_debt_registry == 0):
                            self.add_audit_trail(result, "DebtInRegistry", 0,
                                                 'outstanding debt in registry is 0', 'Accept')
                            result.UW_decision = "Accept"

                        elif(self.loan_applicant_outstanding_debt_in_debt_registry > 0 and self.loan_applicant_outstanding_debt_in_debt_registry < 50):
                            self.add_audit_trail(result, "DebtInRegistry", self.loan_applicant_outstanding_debt_in_debt_registry,
                                                 'outstanding debt in registry between 0 and 50 (both exclusive)', 'Review')
                            result.notification.append("Review Bank Statement")
                            result.UW_decision = "Review"

                        elif(self.loan_applicant_outstanding_debt_in_debt_registry > 50):
                            self.add_audit_trail(result, "DebtInRegistry", self.loan_applicant_outstanding_debt_in_debt_registry,
                                                 'outstanding debt in registry greater than 50', 'Decline')
                            self.UW_decision = "Decline"
                        else:
                            # negative and exact 50
                            pass

                    else:
                        self.add_audit_trail(result, "creditScore", self.loan_applicant_credit_score,
                                             "Credit score greater than 5", 'Decline')
                        self.UW_decision = "Decline"

            elif(self.loan_application_product_name == 'top_up'):
                # redundant
                if(age > 80):
                    self.notification = "Review birthdate and documents of Applicant"

                else:
                    if(self.loan_applicant_credit_score <= 20):
                        self.add_audit_trail(result, 'creditScore', self.loan_applicant_credit_score,
                                             'Credit score between 0 and 20 (inclusive)', 'Accept')
                        self.UW_decision = "Accept"

                    else:
                        self.add_audit_trail(result, 'creditScore', self.loan_applicant_credit_score,
                                             'Credit score greater than 20', 'Decline')
                        self.UW_decision = "Decline"

            else:
                if(self.loan_applicant_credit_score <= 5):
                    self.add_audit_trail(result, "creditScore", self.loan_applicant_credit_score,
                                            "Credit score below or equal 5")

                    # none type handle
                    if(self.loan_applicant_outstanding_debt_in_debt_registry == 0):
                        self.add_audit_trail(result, "DebtInRegistry", 0,
                                                'outstanding debt in registry is 0', 'Accept')
                        result.UW_decision = "Accept"

                    elif(self.loan_applicant_outstanding_debt_in_debt_registry > 0 and self.loan_applicant_outstanding_debt_in_debt_registry < 50):
                        self.add_audit_trail(result, "DebtInRegistry", self.loan_applicant_outstanding_debt_in_debt_registry,
                                                'outstanding debt in registry between 0 and 50 (both exclusive)', 'Review')
                        result.notification.append("Review Bank Statement")
                        result.UW_decision = "Review"

                    elif(self.loan_applicant_outstanding_debt_in_debt_registry > 50):
                        self.add_audit_trail(result, "DebtInRegistry", self.loan_applicant_outstanding_debt_in_debt_registry,
                                                'outstanding debt in registry greater than 50', 'Decline')
                        result.UW_decision = "Decline"
                    else:
                        # negative and exact 50
                        pass

                else:
                    self.add_audit_trail(result, "creditScore", self.loan_applicant_credit_score,
                                            "Credit score greater than 5", 'Decline')
                    result.UW_decision = "Decline"
        return result


external_data = {
    "loan_application_product_name": "wer",
    "loan_application_sum": 600,
    "loan_application_timestamp": "2020-10-18T10:20:30",
    "loan_application_duration_in_days": 90,
    "loan_application_is_top_up": False,
    "loan_applicant_fullname": "Alice Smith",
    "loan_applicant_birthdate": "1988-01-05",
    "loan_applicant_credit_score": 2.3,
    "loan_applicant_income": 1241.0,
    "loan_applicant_liabilities": 312.6,
    "loan_applicant_outstanding_debt_in_debt_registry": 4.32,
    "loan_applicant_is_repeat_client": False
}

user1 = User(**external_data)
print(asdict(user1.application_checker()))
# print(asdict(user1))
