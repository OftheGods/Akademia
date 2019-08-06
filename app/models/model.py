
from difflib import SequenceMatcher


def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()


laptops = []  

class Laptop:
    def __init__(self,name,image,price=0,rental=0,num=0,description=[]):
        self.name = name
        self.image = image
        self.price=price
        self.rental=rental
        self.id=num
        self.description=description

    


            
            
        
        
     
x=1       

Laptop_1=Laptop('Acer Aspire 5', 'https://images-na.ssl-images-amazon.com/images/I/81ecPpDIh%2BL._SL1500_.jpg',1450.00,25,0,"The Dell XPS 13 (2019)")
Laptop_2=Laptop('HP 15z', 'https://images-na.ssl-images-amazon.com/images/I/61%2BYjO3x7bL._SL1000_.jpg',1585.00,30,1)
Laptop_3=Laptop('Dell Inspiron 3000', 'https://images-na.ssl-images-amazon.com/images/I/61SGTPVClFL._SL1000_.jpg',1600.00,28,2)
Laptop_4=Laptop('Lenovo Ideapad 330S', 'https://images-na.ssl-images-amazon.com/images/I/41msLXYG6mL.jpg',950.00,32,3)
Laptop_5=Laptop('Dell Inspiron 5575', 'https://images-na.ssl-images-amazon.com/images/I/71IejwEL2BL._SL1500_.jpg',1200.00,26,4)
Laptop_6=Laptop('Dell Inspiron 3580', 'https://images-na.ssl-images-amazon.com/images/I/61CLFKt2wlL._SL1000_.jpg',1522.62,34,5)
Laptop_7=Laptop('Surface Go 8GB RAM', 'https://images-na.ssl-images-amazon.com/images/I/61vAmTmH3FL._SL1200_.jpg',1169.00,20,6)
Laptop_8=Laptop('HP Envy x360','https://images-na.ssl-images-amazon.com/images/I/81JkfTSj5jL._SL1500_.jpg',940.00,27,7)
Laptop_9=Laptop('Acer Swift 3','https://images-na.ssl-images-amazon.com/images/I/71SM4fSRzzL._SL1500_.jpg',694.70,35,8)
Laptop_10=Laptop('Acer Switch 3','https://images-na.ssl-images-amazon.com/images/I/A1p38mDCdfL._SL1500_.jpg',430.00,31,9)







laptops.append(Laptop_1)
laptops.append(Laptop_2)
laptops.append(Laptop_3)
laptops.append(Laptop_4)
laptops.append(Laptop_5)
laptops.append(Laptop_6)
laptops.append(Laptop_7)
laptops.append(Laptop_8)
laptops.append(Laptop_9)
laptops.append(Laptop_10)

def add_list(lst):
    for i in laptops:
        lst.append(i)

def total_price(rental,months):
    months = int(months)
    return round(rental*months,2)
    

def return_results(search_id):
    global laptops
    results = []
    if search_id == 'View our Laptops':
        for i in laptops:
            results.append({'name':i.name,'image':i.image,'price':i.price,'rental':i.rental,'id':i.id})
    elif not search_id:
        for i in laptops:
            results.append({'name':i.name,'image':i.image,'price':i.price,'rental':i.rental,'id':i.id})
    else:
        for i in laptops:
            up=i.name.upper()
            search_id=search_id.upper()
            similarity=similar(up,search_id)
            if similarity >0.3:
                results.append({'name':i.name,'image':i.image,'price':i.price,'rental':i.rental,'id':i.id})
        
        if not results:
                return 'None'
    return results

def return_credit(num):
    num = str(num)
    return("*"*12+num[12:16])


    
    