

node = 0
action = {1,2,3}

def rec(count):
    util = 0
    if count ==0:
        return util
    
    util += rec(count-1) 
    
   
        
        
print(rec(5))
    
    