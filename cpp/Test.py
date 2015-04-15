import sys
import os
def os_type():
  print sys.platform[:-1] 
  return os.uname()[0].lower()

def add(a ,b):
  return a + b

def TestDict(dict):  
  print dict  
  dict["Age"] = 17  
  return dict  

class Person:  
  def greet(self, greetStr):  
    print greetStr  

if __name__ == "__main__":
  os_type()
