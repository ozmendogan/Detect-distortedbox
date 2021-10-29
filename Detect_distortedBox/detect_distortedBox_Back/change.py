import os


current="1"

def changeOnes():
    current="1"
    new = "0"
 
    with open("onezero.txt","r",encoding="utf-8") as file :
        result = file.read()
    
    result = result.replace(current,new)
    with open("onezero.txt","w",encoding="utf-8") as newfile :
        newfile.write(result)
    

def changeZeros():
    current="0"
    new = "1"
 
    with open("onezero.txt","r",encoding="utf-8") as file :
        result = file.read()
    
    result = result.replace(current,new)
    with open("onezero.txt","w",encoding="utf-8") as newfile :
        newfile.write(result)
    
    
def readValue():
    with open("onezero.txt","r",encoding="utf-8") as file :
        result = file.read()
    return result
    