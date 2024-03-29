from app import app
from flask import render_template, request, redirect, session, url_for
from app.models import model, formopener


from flask_pymongo import PyMongo
import random
import time
import datetime
from datetime import date

app.secret_key= b'\xe1s\xf1\xad\xccA\xd7\x89\x8e\xde\xe14)\x08\x90\x85'
app.config['MONGO_DBNAME'] = 'computer_accounts'
app.config['MONGO_URI'] ='mongodb+srv://admin:LxVreieNzqk568n@cluster0-0ytxr.mongodb.net/computer_accounts?retryWrites=true&w=majority'
mongo = PyMongo(app)

laptop_page=[]
username=None
address=None
credit=None
picture = None
credit_show=None
error=None
months=None
my_orders = None
all_laptops=[]
laptops=[]
model.add_list(all_laptops)
@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    global username
    global laptops
    global address
    global credit
    global credit_show
    global error
    global picture
    global my_orders
    if request.method=='POST':
        user_data = request.form
        print(user_data)
        accounts=mongo.db.accounts
        existing_user=accounts.find_one({"username":user_data['username']})
        if user_data['sign/log'] == 'Log In':
            if existing_user:
                if existing_user['password']==user_data['pass']:
                    username = existing_user['username']
                    session['username'] = existing_user['username']
                    session['address'] = existing_user['address']
                    session['credit'] = existing_user['credit']
                    session['error'] = None
                    session['credit_show'] = None
                    address=None
                    if existing_user['address']:
                        address=existing_user['address']
                    credit=None
                    if existing_user['credit']:
                        credit=existing_user['credit']
                        credit_show=model.return_credit(credit['Credit'])
                    picture=None
                    if existing_user['picture']:
                        picture = existing_user['picture']
                    orders=mongo.db.orders
                    existing_orders=orders.find_one({"username":user_data['username']})
                    if existing_orders:
                        my_orders = existing_orders
                    session['error'] = None
                    error=None
                    return redirect(url_for('index'))
    
                else:
                    session['error'] = "Incorrect Password"
                    error="Incorrect Password"
                    return redirect('/login')
            else:
                error="User doesn't exist"
                return redirect('/login')
        else:
            if existing_user:
                error="Username is taken"
                return redirect('/sign_up')
            else:
                accounts.insert({"username":user_data['username'],"password":user_data['pass'],"address":None,"credit":None,"picture":None})
                session['username'] = user_data['username']
                session['loggedin'] = True
                username= user_data['username']
                error=None
                return redirect(url_for('index'))
        
                
        
    else:
        error=None
        return render_template('index.html',laptops=laptops,username=username,picture=picture)

@app.route('/results',methods=['GET','POST'])
def results():
    global all_laptops
    laptops=[]
    if request.method=='POST':
        user_data = request.form
        user_search = user_data['search']
        laptops = model.return_results(user_search)
        if laptops == 'None':
            return render_template('results.html',user_search=user_search)
        return render_template('results.html',user_search=user_search,laptops=laptops)
    else:
        return redirect('/index')


@app.route('/laptop/<laptop>')
def laptop(laptop):
    global laptop_page
    global laptops
    laptop = int(laptop)
    laptop_page = all_laptops[laptop]
    return render_template('laptops.html',laptop_page=laptop_page)

@app.route('/checkout',methods=['GET','POST'])
def checkout():
    global address
    global months
    global months_left
    if request.method == 'POST':
        userdata=request.form
        months = userdata['months']
        months_left = int(userdata['months'])
        if not address:
            return render_template('checkout.html')
        else:
            return redirect('/checkout2')
    else:
        return redirect('/index')

@app.route('/checkout2',methods=['GET','POST'])
def checkout2():
    global address
    global credit
    if request.method=='POST':
        address=request.form
        if not credit:
            return render_template('checkout2.html')
        else:
            return redirect('/confirmation')
    else:
        if not credit:
            return render_template('checkout2.html')
        else:
            return redirect('/confirmation')



            
@app.route('/sign_up')
def sign_up():
    global error
    return render_template('sign_up.html',error=error)

@app.route('/login')
def login():
    global error
    return render_template('login.html',error=error)

@app.route('/confirmation',methods=['GET','POST'])
def final_checkout():
    global credit
    global address
    global credit_show
    global laptop_page
    global months
    total=model.total_price(30,months)
    if request.method =='POST':
        print (address)
        credit=request.form
        print(credit)
        credit_show=model.return_credit(credit['Credit'])
        return render_template('confirmation.html',laptop_page=laptop_page,credit=credit,address=address,credit_show=credit_show,total=total)
    else:
        return render_template('confirmation.html',laptop_page=laptop_page,credit=credit,address=address,credit_show=credit_show,total=total)

@app.route('/success')
def success():
    global laptop_page
    global username
    global months
    global months_left
    orders = mongo.db.orders
    order_num = random.randrange(100000,999999)
    if not username:
        orders.insert({"ID":order_num,"months":months,"months_left":months_left,"order_date":time.strftime("%x"),"order_renew":datetime.date.today().strftime("%d"),"order_name":laptop_page.name,"order_id":laptop_page.id,"order_image":laptop_page.image,"order_rental":laptop_page.rental,"status":"Active"})
    else:
        orders.insert({"username":username,"ID":order_num,"months":months,"months_left":months_left,"order_date":time.strftime("%x"),"order_date":time.strftime("%x"),"order_renew":datetime.date.today().strftime("%d"),"order_name":laptop_page.name,"order_id":laptop_page.id,"order_image":laptop_page.image,"order_rental":laptop_page.rental,"status":"Active"})
        
    return render_template('success.html',order_num=order_num)

@app.route('/accounts/<username_>', methods=['GET','POST'])
def accounts(username_):
    global address
    global credit
    global credit_show
    global username
    global picture
    global my_orders
    if request.method=='POST':
        userdata=request.form
        if userdata['Location/Credit'] == "Add New Location":
            address=userdata
            accounts=mongo.db.accounts
            user = accounts.find_one({"username":username_})
            computer_accounts=mongo.db
            computer_accounts.accounts.update({"username":username_},{"username":username_,"address":userdata,"password":user['password'],"credit":user["credit"],"picture":user["picture"]})
        elif userdata['Location/Credit'] == "Add Profile Pic":
            picture=userdata
            print(picture)
            accounts=mongo.db.accounts
            user = accounts.find_one({"username":username_})
            computer_accounts=mongo.db
            computer_accounts.accounts.update({"username":username_},{"username":username_,"address":user['address'],"password":user['password'],"credit":user["credit"],"picture":userdata})
        elif userdata['Location/Credit'] == "Unactive":
            computer_accounts=mongo.db
            orders=mongo.db.orders
            existing_orders=orders.find_one({'username':username_})
            computer_accounts.orders.update({"ID":existing_orders['ID']},{"username":existing_orders['username'],"ID":existing_orders['ID'],"months":existing_orders['months'],"months_left":existing_orders['months_left'],"order_date":existing_orders['order_date'],"order_renew":existing_orders['order_renew'],"order_name":existing_orders['order_name'],"order_id":existing_orders['order_id'],"order_image":existing_orders['order_image'],"order_rental":existing_orders['order_rental'],"status":"Unactive"})
        elif userdata['Location/Credit'] == "Active":
            computer_accounts=mongo.db
            orders=mongo.db.orders
            existing_orders=orders.find_one({'username':username_})
            computer_accounts.orders.update({"ID":existing_orders['ID']},{"username":existing_orders['username'],"ID":existing_orders['ID'],"months":existing_orders['months'],"months_left":existing_orders['months_left'],"order_date":existing_orders['order_date'],"order_renew":existing_orders['order_renew'],"order_name":existing_orders['order_name'],"order_id":existing_orders['order_id'],"order_image":existing_orders['order_image'],"order_rental":existing_orders['order_rental'],"status":"Active"})
        else:
            credit=userdata
            accounts=mongo.db.accounts
            user = accounts.find_one({"username":username_})
            computer_accounts=mongo.db
            computer_accounts.accounts.update({"username":username_},{"username":username_,"address":user['address'],"password":user['password'],"picture":user['picture'],"credit":userdata})
            credit_show=model.return_credit(credit['Credit'])
        return redirect('/accounts/'+username)
    else:
        orders=mongo.db.orders
        existing_orders=orders.find_one({"username":username_})
        if existing_orders:
            my_orders = existing_orders
        return render_template('account_page.html',address=address,username=username,credit=credit,credit_show=credit_show,picture=picture,my_orders=my_orders)

@app.route('/add_location')
def add_location():
    return render_template('add_location.html',address=address,username=username)

@app.route('/add_credit')
def add_credit():
    return render_template('add_credit.html',credit=credit,username=username)

@app.route('/add_picture')
def add_picture():
    return render_template('add_picture.html',username=username)

@app.route('/change_picture')
def change_picture():
    global picture
    global username
    picture = None
    accounts=mongo.db.accounts
    user = accounts.find_one({"username":username})
    computer_accounts=mongo.db
    computer_accounts.accounts.update({"username":username},{"username":username,"address":user['address'],"password":user['password'],"credit":user["credit"],"picture":None})
    return redirect('/add_picture')

@app.route('/change_address')
def change_address():
    global address
    global username
    address=None
    accounts=mongo.db.accounts
    user = accounts.find_one({"username":username})
    computer_accounts=mongo.db
    computer_accounts.accounts.update({"username":username},{"username":username,"address":None,"password":user['password'],"credit":user["credit"],"picture":user['picture']})
    return redirect('/add_location')

@app.route('/change_credit')
def change_credit():
    global credit
    global username
    credit=None
    accounts=mongo.db.accounts
    user = accounts.find_one({"username":username})
    computer_accounts=mongo.db
    computer_accounts.accounts.update({"username":username},{"username":username,"address":user['address'],"password":user['password'],"credit":None,"picture":user['picture']})
    return redirect('/add_credit')

@app.route('/change_status')
def change_status():
    global my_orders
    global username
    print(my_orders)
    return render_template('change_status.html',my_orders=my_orders,username=username)

@app.route('/logout')
def logout():
    global username
    global address
    global credit
    global credit_show
    global picture
    address=None
    username=None
    credit=None
    credit_show=None
    picture=None
    
    return redirect('/index')
    
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')
    



