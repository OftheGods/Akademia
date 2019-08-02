
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

Laptop_1=Laptop('Dell XPS 13', 'https://images-na.ssl-images-amazon.com/images/I/71UT3GpjVQL._SL1280_.jpg',1450.00,0,0,"The Dell XPS 13 (2019)")

    




Laptop_2=Laptop('Dell XPS 15', 'https://images-na.ssl-images-amazon.com/images/I/81Yd-xXWdcL._SL1500_.jpg',1585.00,0,1)
Laptop_3=Laptop('Apple Macbook Pro', 'https://images-na.ssl-images-amazon.com/images/I/61SJu997CCL._SL1500_.jpg',1600.00,0,2)
Laptop_4=Laptop('Apple Macbook Air', 'https://images-na.ssl-images-amazon.com/images/I/51xZz6jSHSL._SL1024_.jpg',950.00,0,3)
Laptop_5=Laptop('Huawei Matebook 13', 'https://images-na.ssl-images-amazon.com/images/I/51XMAo9vzHL._SL1000_.jpg',1200.00,0,4)
Laptop_6=Laptop('Huawei Matebook X Pro', 'https://c1.neweggimages.com/ProductImage/34-324-031-V07.jpg',1522.62,0,5)
Laptop_7=Laptop('HP Spectre x360', 'https://images-na.ssl-images-amazon.com/images/I/717iiI8wWxL._SL1500_.jpg',1169.00,0,6)
Laptop_8=Laptop('HP Envy x360','https://images-na.ssl-images-amazon.com/images/I/81JkfTSj5jL._SL1500_.jpg',940.00,0,7)
Laptop_9=Laptop('Acer Swift 3','https://images-na.ssl-images-amazon.com/images/I/71SM4fSRzzL._SL1500_.jpg',694.70,0,8)
Laptop_10=Laptop('Acer Switch 3','https://images-na.ssl-images-amazon.com/images/I/A1p38mDCdfL._SL1500_.jpg',430.00,0,9)







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
    


def return_results(search_id):
    global laptops
    results = []
    if search_id == 'View our Laptops':
        for i in laptops:
            results.append({'name':i.name,'image':i.image,'price':i.price,'rental':i.rental,'id':i.id})
    else:
        for i in laptops:
            up=i.name.upper()
            search_id=search_id.upper()
            similarity=similar(up,search_id)
            if similarity >0.4:
                results.append({'name':i.name,'image':i.image,'price':i.price,'rental':i.rental,'id':i.id})
        
        if not results:
                return 'None'
    return results

def return_credit(num):
    num = str(num)
    return("*"*12+num[12:16])


    
    