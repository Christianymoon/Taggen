# class make for Christian Vergara and VR Cybersecurity 
# pragma python usameasure.py

from fractions import Fraction

class footwear():
     
    #USA METHODS  
     
    def to_usa(number):
        if number > 20 and number < 30:
            return number % 20 + 1 
        elif number >= 30:
            return number % 30 + 11
            
    def if_int(number):
        if number - round(number) != 0:
            return number
        return int(number)
               
    #MEX METHODS
    def to_mex(number):
        if number >= 5 and number <= 16:
            footwear = number - 1 
            footwear += 20
            if number - round(number) != 0:
                return str(int(footwear)) + "    "
            return int(footwear)
        
    def if_fraction(number):
        if number >= 5 and number <= 16:
            footwear = number - 1 
            footwear += 20
            if number - round(number) != 0:
                return "½"
            return ""
 
            
if __name__ == "__main__":
    pass

    