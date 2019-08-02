from app import app
from flask import render_template, request, redirect, session, url_for
from app.models import model, formopener


from flask_pymongo import PyMongo

app.secret_key= b'\xe1s\xf1\xad\xccA\xd7\x89\x8e\xde\xe14)\x08\x90\x85'
app.config['MONGO_DBNAME'] = 'computer_accounts'
app.config['MONGO_URI'] ='mongodb+srv://admin:LxVreieNzqk568n@cluster0-0ytxr.mongodb.net/computer_accounts?retryWrites=true&w=majority'
mongo = PyMongo(app)

laptop_page=[]
username=''
address=''
credit='s'
all_laptops=[]
laptops=[]
model.add_list(all_laptops)
@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    global username
    global laptops
    if request.method=='POST':
        user_data = request.form
        print(user_data)
        accounts=mongo.db.accounts
        existing_user=accounts.find_one({"username":user_data['username']})
        if user_data['sign/log'] == 'Log In':
            if existing_user:
                if existing_user['password']==user_data['pass']:
                    session['username'] = existing_user['username']
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
                accounts.insert({"username":user_data['username'],"password":user_data['pass']})
                session['username'] = user_data['username']
                session['loggedin'] = True
                username= existing_user['username']
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
    return render_template('checkout.html')

@app.route('/checkout2',methods=['GET','POST'])
def checkout2():
    global address
    if request.method=='POST':
        address=request.form
        return render_template('checkout2.html')
    else:
        return redirect ('/index')



            
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/confirmation',methods=['GET','POST'])
def final_checkout():
    if request.method =='POST':
        global credit
        global address
        global laptop_page
        print (address)

        credit=request.form
        print(credit)
        credit_show=model.return_credit(credit['Credit'])
        return render_template('confirmation.html',laptop_page=laptop_page,credit=credit,address=address,credit_show=credit_show)
    else:
        return redirect('/index')

@app.route('/success')
def success():
    return render_template('success.html')
