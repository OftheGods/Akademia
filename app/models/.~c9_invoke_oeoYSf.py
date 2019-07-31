


from difflib import SequenceMatcher


def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()


laptops = []  

class Laptop:
    def __init__(self,name,image,price=0,rental=0,num=0):
        self.name = name
        self.image = image
        self.price=price
        self.rental=rental
        self.id=num

    

            
            
        
        
     
x=1       

Laptop_1=Laptop('Dell XPS 13', 'https://images-na.ssl-images-amazon.com/images/I/71UT3GpjVQL._SL1280_.jpg',1450.00,0,0)
Laptop_2=Laptop('Dell XPS 15', 'https://images-na.ssl-images-amazon.com/images/I/81Yd-xXWdcL._SL1500_.jpg',1585.00,0,1)
Laptop_3=Laptop('Apple Macbook Pro', 'https://images-na.ssl-images-amazon.com/images/I/61SJu997CCL._SL1500_.jpg',1600.00,0,2)
Laptop_4=Laptop('Apple Macbook Air', 'https://images-na.ssl-images-amazon.com/images/I/51xZz6jSHSL._SL1024_.jpg',950.00,0,3)







laptops.append(Laptop_1)
laptops.append(Laptop_2)
laptops.append(Laptop_3)

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
            if similarity >0.25:
                results.append({'name':i.name,'image':i.image,'price':i.price,'rental':i.rental,'id':i.id})
        
        if not results:
                return 'None'
    return results

