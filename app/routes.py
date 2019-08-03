from app import app
from flask import render_template, request, redirect, session, url_for
from app.models import model, formopener


from flask_pymongo import PyMongo

app.secret_key= b'\xe1s\xf1\xad\xccA\xd7\x89\x8e\xde\xe14)\x08\x90\x85'
app.config['MONGO_DBNAME'] = 'computer_accounts'
app.config['MONGO_URI'] ='mongodb+srv://admin:LxVreieNzqk568n@cluster0-0ytxr.mongodb.net/computer_accounts?retryWrites=true&w=majority'
mongo = PyMongo(app)

laptop_page=[]
username=None
address=None
credit=None
credit_show=None
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
    if request.method=='POST':
        user_data = request.form
        print(user_data)
        accounts=mongo.db.accounts
        existing_user=accounts.find_one({"username":user_data['username']})
        if user_data['sign/log'] == 'Log In':
            if existing_user:
                if existing_user['password']==user_data['pass']:
                    session['username'] = existing_user['username']
                    if existing_user['address']:
                        address=existing_user['address']
                    if existing_user['credit']:
                        credit=existing_user['credit']
                        credit_show=model.return_credit(credit['Credit'])
                    username = existing_user['username']
                    return redirect(url_for('index'))
    
                else:
                    return 'Invalid password'
            else:
                return "User doesn't exist"
        else:
            if existing_user:
                return 'Username is taken'
            else:
                accounts.insert({"username":user_data['username'],"password":user_data['pass'],"address":None,"credit":None})
                session['username'] = user_data['username']
                session['loggedin'] = True
                username= user_data['username']
                return redirect(url_for('index'))
        
                
        
    else:
        return render_template('index.html',laptops=laptops,username=username)

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

@app.route('/checkout')
def checkout():
    global address
    if not address:
        return render_template('checkout.html')
    else:
        return redirect('/checkout2')

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
    return render_template('sign_up.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/confirmation',methods=['GET','POST'])
def final_checkout():
    global credit
    global address
    global credit_show
    global laptop_page
    if request.method =='POST':
        print (address)

        credit=request.form
        print(credit)
        credit_show=model.return_credit(credit['Credit'])
        return render_template('confirmation.html',laptop_page=laptop_page,credit=credit,address=address,credit_show=credit_show)
    else:
        return render_template('confirmation.html',laptop_page=laptop_page,credit=credit,address=address,credit_show=credit_show)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/accounts/<username_>', methods=['GET','POST'])
def accounts(username_):
    global address
    global credit
    global credit_show
    global username
    if request.method=='POST':
        userdata=request.form
        if userdata['Location/Credit'] == "Add New Location":
            address=userdata
            accounts=mongo.db.accounts
            user = accounts.find_one({"username":username_})
            computer_accounts=mongo.db
            computer_accounts.accounts.update({"username":username_},{"username":username_,"address":userdata,"password":user['password'],"credit":user["credit"]})
        else:
            credit=userdata
            accounts=mongo.db.accounts
            user = accounts.find_one({"username":username_})
            computer_accounts=mongo.db
            computer_accounts.accounts.update({"username":username_},{"username":username_,"address":user['address'],"password":user['password'],"credit":userdata})
            credit_show=model.return_credit(credit['Credit'])
        return redirect('/accounts/'+username)
    else:
        return render_template('account_page.html',address=address,username=username,credit=credit,credit_show=credit_show)

@app.route('/add_location')
def add_location():
    return render_template('add_location.html',address=address,username=username)

@app.route('/add_credit')
def add_credit():
    return render_template('add_credit.html',credit=credit,username=username)

@app.route('/logout')
def logout():
    global username
    global address
    global credit
    global credit_show
    address=None
    username=None
    credit=None
    credit_show=None
    
    return redirect('/index')
    



