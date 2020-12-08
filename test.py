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
    userOutput: dict
      
    
    
       
    
    def __post_init__(self):
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
