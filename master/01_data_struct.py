"""TEST"""
import os

def base_type():
    """_summary_
    """
    # def hex(__number: int | SupportsIndex) -> str:
    stats = os.stat("./")
    print(stats.st_ino) #0xff
    print(hex(stats.st_ino)[2:]) #0xff
    print(hex(255)) #0xff

if __name__=="__main__":
    base_type()
   
    