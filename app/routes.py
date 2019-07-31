from app import app
from flask import render_template, request, redirect, session, url_for
from app.models import model, formopener


from flask_pymongo import PyMongo

app.secret_key= b'\xe1s\xf1\xad\xccA\xd7\x89\x8e\xde\xe14)\x08\x90\x85'
app.config['MONGO_DBNAME'] = 'computer_accounts'
app.config['MONGO_URI'] ='mongodb+srv://admin:LxVreieNzqk568n@cluster0-0ytxr.mongodb.net/computer_accounts?retryWrites=true&w=majority'
mongo = PyMongo(app)

username=''
laptops=[]
model.add_list(laptops)
@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    global username
    if request.method=='POST':
        user_data = request.form
        if user_data['sign/log'] == 'Sign In':
            username = user_data['username']
            password=user_data['pass']
            accounts=mongo.db.accounts
            existing_user=accounts.find_one({"username":username})
            if existing_user is None:
                accounts.insert({'username':username,'password':password})
                session['username'] = username
                return redirect('/index')
            else:
                return redirect('/index')
        else:
            username = user_data['username']
            password=user_data['pass']
            accounts=mongo.db.accounts
            existing_user=accounts.find_one({"username":username})
            if existing_user is None:
                return redirect('/index')
            else:
                if existing_user['password'] == password:
                    session['username'] = username
                    return redirect('/index')
                
            
    else:
        return render_template('index.html',laptops=laptops,username=username)

@app.route('/results',methods=['GET','POST'])
def results():
    global laptops
    laptops=[]
    if request.method=='POST':
        user_data = request.form
        user_search = user_data['search']
        laptops = model.return_results(user_search)
        if laptops == 'None':
            return render_template('no_results.html')
        return render_template('results.html',user_search=user_search,laptops=laptops)
    else:
        return redirect('/index')


@app.route('/laptop/<laptop>')
def laptop(laptop):
    global laptops
    laptop = int(laptop)
    laptop_page = laptops[laptop]
    return render_template('laptops.html',laptop_page=laptop_page)

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    global laptops
    if request.method=='POST':
        user_data = request.form
        if user_data['buy_rent']=='Buy Item':
            return render_template('checkout.html',laptops=laptops)
        elif user_data['buy_rent'] =='Rent Item':
            return render_template('rentout.html',laptops=laptops)
        else:
            return 'Hah noob'
    else:
        return redirect('/index')

@app.route('/success', methods=['GET','POST'])
def success():
    global laptops
    if request.method=='POST':
        user_data = request.form
        if user_data['submit']=='Buy':
            return 'You have successfully purchased the '+laptops[0]['name']+' for $'+str(laptops[0]['price'])
        elif user_data['submit'] =='Rent':
            total_price = round(float(user_data['months'])*float(laptops[0]['rental']),2)
            return 'You have successfully rented the '+laptops[0]['name']+' for $'+str(total_price)+' over '+str(user_data['months']+' months')
            
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/login')
def login():
    return render_template('login.html')
