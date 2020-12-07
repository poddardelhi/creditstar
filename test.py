from datetime import date, datetime, timedelta
from typing import List, Tuple,Dict,Optional
from pydantic import BaseModel
from dataclasses import dataclass,asdict




@dataclass
class User:
    firstname: str
    lastname: str
    age: int
    notification:str
    
    
    '''
    def __init__(self):
        self.firstname=input("Enter your name:")
        self.lastname=input("Enter the last name:")
        self.age=int(input("Enter the age:"))
       ''' 
    
    def test_checker(self):
        age= int(self.age)
        if(age<30):
            self.notification="Young"
        elif (age in range(30,45)):
            self.notification="Mid Aged"
        elif (age in range(46,60)):
            self.notification= "Aged"
        else:
            self.notification="old"

external_data={
    'firstname':'nishant',
    'lastname': 'poddar',
    'age': '89',
    'notification': None
}
            
user1=User(**external_data)
user1.test_checker()
print(asdict(user1)) 
