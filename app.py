from flask import Flask,request,jsonify,render_template,session,flash
from flask_restful import Api
from database import db
from resources import routes
from database.model import  cart, products, gift,user,membership,contact_
import time, random
from datetime import date
import datetime
import argon2
from cryptography.fernet import Fernet
# Hash a password
def Argon_Encrypt(password):
    hasher = argon2.PasswordHasher()
    Encrypted_content = hasher.hash(password)
    return Encrypted_content

# Verify a password attempt
def verify_password(Encrypted_content, verifier):
    hasher = argon2.PasswordHasher()
    try:
        hasher.verify(Encrypted_content, verifier)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
# Flask instance create
app = Flask(__name__)
app.secret_key="xyz"
# # Flask instance and mongo db url configuration
app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost:27017/web_project'}
# # flask API instance creation
db.initialize_db(app)
api = Api(app)
routes.initialize_routes(api)

# Set the session lifetime to 1 hour
app.config['PERMANENT_SESSION_LIFETIME'] = 3600


@app.route('/')
def hello_world():  # put application's code here
    try:
        if session["email"] != None:
            return render_template("index.html")
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")


@app.route('/index')
def index():
    try:
        if session["email"] != None:
            return render_template("index.html")
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signupAction',methods=["POST"])
def signupAction():
    name = request.form["Name"]
    email = request.form["Email"]
    pwd = request.form["Password"]
    phon = request.form["phone"]
    add = request.form["address"]
    # Hash the password
    Encrypted_content = Argon_Encrypt(pwd)
    obj = user(username = name,email = email,password = Encrypted_content,phone = phon,address=add).save()
    if (obj):
        session["email"] = Argon_Encrypt(email);
        session["name"] = Argon_Encrypt(name);
        session["pwd"] = Argon_Encrypt(pwd);
    return render_template("index.html")

@app.route('/loginAction',methods=["POST"])
def loginAction():
    email = request.form["Email"]
    pwd = request.form["Password"]
    obj = user.objects(email = email)
    if (obj):
        pwd_in_db = obj[0]["password"]
        is_password_valid = verify_password(pwd_in_db, pwd)
        if(is_password_valid):
            session["email"] = Argon_Encrypt(email);
            session["name"] = Argon_Encrypt(obj[0]["username"]);
            session["pwd"] = Argon_Encrypt(pwd);
            if email == "admin@gmail.com":
                return render_template("adminpanel.html")
            else:
                return render_template("index.html")
        else:
            return render_template("login.html", error="User does not exit")
    else:
        return render_template("login.html", error="User does not exit at key")


@app.route('/getproduct')
def getproducts():
    try:
        if session["email"] != None:
            return render_template("product.html");
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")

@app.route('/gettrack')
def gettrack():
    try:
        if session["email"] != None:
            obj = products.objects(category="perfume")
            return render_template("tracking.html", product=obj)
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")

@app.route('/getclothes')
def getclothes():
    try:
        if session["email"] != None:
            obj = products.objects(category="clothes")
            return render_template("clothes.html",product = obj)
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/getaccessories')
def getaccessories():
    try:
        if session["email"] != None:
            obj = products.objects(category="accessories")
            return render_template("accessories.html",product=obj)
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/getwatches')
def getwatches():
    try:
        if session["email"] != None:
            obj = products.objects(category="watches")
            return render_template("watches.html", product=obj)
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/getperfumes')
def getperfumes():
   try:
       if session["email"] != None:
           obj = products.objects(category="perfumes")
           return render_template("perfumes.html",product=obj)
       else:
           return render_template("index.html")
   except Exception as e:
       return render_template("login.html")
@app.route('/getfaq')
def getfaq():
    try:
        if session["email"] != None:
            return render_template("faq.html")
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/contact')
def contact():
    try:
        if session["email"] != None:
            return render_template("contact.html")
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/about')
def about():
    try:
        if session["email"] != None:
            return render_template("about.html")
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/contactaction',methods=["POST"])
def contactaction():
    # try:
        if session["email"] != None:
            a1=request.form["name"]
            a2=request.form["email"]
            a3=request.form["message"]
            obj = contact_(cont_name=a1, cont_email=a2, cont_message=a3).save()
            return render_template("index.html")
        else:
            return render_template("login.html")
    # except Exception as e:
    #      return render_template("login.html")

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime.datetime(year, month, day)
@app.route('/getmembership')
def getmembership():
    try:
        if session["email"] != None:
            return render_template("membership.html")
        else:
            return render_template("login.html")
    except Exception as e:
         return render_template("login.html")
@app.route('/add_membership/<category>/<duration>')
def add_membership(category,duration):
    if session["email"] != None:
        # Calculate the start and end dates
        start_date = datetime.datetime.now()
        duration = int(duration)
        end_date = add_months(start_date, duration)

        # Save the membership to MongoDB
        member = {
            'email': session.get("email"),
            # 'email': session["email"],
            'category': category,
            'start_date': start_date,
            'end_date': end_date
        }
        membership(**member).save()

        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/add2cart/<category>/<name>')
def add2cart(category,name):
    # try:
        if session.get("email") != None:
            obj = products.objects(category = category,prod_name=name).first()
            timestamp = int(time.time() * 1000)
            random_num = random.randint(1000, 9999)
            cart_id = f"cart_{timestamp}_{random_num}"
            data1 = cart.objects()
            data2 = cart.objects(prodname=name).first()
            uname =  session.get("name")
            tamount = 0
            if data1:
                if data2:
                    cart.objects(prodname=name).update(quantity=int(data2["quantity"])+1)
                else:
                    cart(cartid=data1[0]["cartid"], username=uname, prodname=name, quantity=1,
                         amount=float(obj["prod_price"])).save()
            else:
                if data2:
                    cart.objects(prodname=name).update(quantity=int(data2["quantity"]) + 1)
                else:
                    cart(cartid=cart_id, username=uname, prodname=name, quantity=1,
                         amount=obj["prod_price"]).save()
            data = cart.objects()
            for i in data:
                tamount+=int(i["amount"] * i["quantity"])
            return render_template("cart.html",cartitems = data, totalamount=tamount)
        else:
            return render_template("login.html", error = "Please login!!")
    # except Exception as e:
    #     return render_template("login.html", error= str(e))

@app.route('/payoptionform',  methods=["POST"])
def payoptionform():
    try:
        paymethod=request.form["payment"]
        if paymethod =="credit_card":
            return render_template("card.html")
        else:
            email=session["email"]
            uname = session["name"]
            data=user.objects(email=email).first()
            tamount = 0
            current_date = date.today().strftime('%d/%m/%Y')
            cartitems = cart.objects()
            for i in cartitems:
                tamount += (i.quantity * i.amount)
                cartid = i.cartid
            oamount=tamount
            d = membership.objects(email = email).first()
            if d:
                if int(d["category"]) == 1:
                    tamount -= (tamount * 0.08)
                elif int(d["category"]) == 2:
                    tamount -= (tamount * 0.15)
                    print(tamount)
                elif int(d["category"]) == 3:
                    tamount -= (tamount * 0.3)
                elif int(d["category"]) == 4:
                    tamount -= (tamount * 0.5)
                else:
                    tamount += (i.quantity *i.amount)
            cart.objects(cartid=cartid).delete()

            return render_template("checkout.html", date=current_date, cartid=cartid, username=uname,
                                   address=data.address, phoneno=data.phone, paymode="COD", cartitems=cartitems,
                                   totalamount=oamount, amounttopay=tamount)
    except Exception as e:
        return render_template("cart.html", error=str(e))


@app.route('/payoptionform2',  methods=["POST"])
def payoptionform2():
    try:
        paymethod=request.form["payment"]
        if paymethod =="credit_card":
            return render_template("card.html")
        else:
            email=session["email"]
            uname = session["name"]
            data=user.objects(email=email).first()
            tamount = 0
            current_date = date.today().strftime('%d/%m/%Y')
            giftitems = gift.objects()
            for i in giftitems:
                tamount += (i.wrapcharges + i.giftprice)
                giftid = i.giftid
            oamount=tamount
            gift.objects(giftid=giftid).delete()

            return render_template("checkout.html", date=current_date, cartid=giftid, username=uname,
                                   address=data.address, phoneno=data.phone, paymode="COD", giftitems=giftitems,
                                   totalamount=oamount, amounttopay=tamount)
    except Exception as e:
        return render_template("cart.html", error=str(e))
@app.route('/checkoutcard', methods=["POST"])
def checkoutcard():
    try:
        if session.get("email")!=None:
            uname=session["name"]
            email = session["email"]
            data=user.objects(email=email).first()
            tamount = 0
            current_date = date.today().strftime('%d/%m/%Y')
            cartitems = cart.objects()
            for i in cartitems:
                tamount += (i.quantity * i.amount)
                cartid= i.cartid
            oamount = tamount
            d = membership.objects(email=email).first()
            if d:
                if int(d["category"]) == 1:
                    tamount -= (tamount * 0.08)
                elif int(d["category"]) == 2:
                    tamount -= (tamount * 0.15)
                    print(tamount)
                elif int(d["category"]) == 3:
                    tamount -= (tamount * 0.3)
                elif int(d["category"]) == 4:
                    tamount -= (tamount * 0.5)
                else:
                    tamount += (i.quantity * i.amount)
            cart.objects(cartid =cartid).delete()
            return render_template("checkout.html", date=current_date, cartid = cartid,username=uname,
                                   address=data.address, phoneno=data.phone,paymode="Credit Card",
                                   cartitems=cartitems, totalamount=oamount, amounttopay=0.0)
        else:
            return render_template("login.html", error="Please login!!")
    except Exception as e:
        return render_template("cart.html")


@app.route('/wrapgiftform')
def wrapgiftform():
    try:
        if session.get("email") != None:
            return render_template("wrapgift.html")
        else:
            return render_template("login.html", error="Please login!!")
    except Exception as e:
        return render_template("wrapgift.html", error=str(e))
@app.route('/wrapgiftcat')
def wrapgiftcat():
    if session["email"] != None:
        category = request.args.get('category')
        return render_template("wrapgiftcat.html", catg=category)
    else:
        return render_template("login.html")

@app.route('/giftwrapdetail', methods=["POST"])
def giftwrapdetail():
    if session["email"] != None:
        category = request.form["category"]
        print("CAST0",category)
        if category == "Birthday":
            wrapcharges = 12
        elif category == "Wedding":
            wrapcharges = 18
        elif category == "General":
            wrapcharges = 9
        giftname = request.form["giftname"]
        name = request.form["rname"]
        mess = request.form["message"]
        wrapqual = request.form["giftwrapopt"]
        if wrapqual == "premium":
            wrapcharges += 2
        elif wrapqual == "vvip":
            wrapcharges += 5
        data = products.objects(prod_name=giftname).first()
        if data:
            amount = data.prod_price
            timestamp = int(time.time() * 1000)
            random_num = random.randint(1000, 9999)
            gift_id = f"cart_{timestamp}_{random_num}"
            data2 = gift.objects(giftname=giftname).first()
            data3 = gift.objects().first()
            if data3 != None:
                if data2 != None:
                    if data2.recpname != name:
                        gift(giftid=data3.giftid, giftname=giftname, giftwrapqual=wrapqual, giftprice=amount,
                             wrapcharges=wrapcharges, recpname=name, giftmess=mess).save()
                    else:
                        flash(
                            "As you are presenting this gift to your beloved ones, we kindly advise against duplicating any items. Instead, we recommend adding different items to the gift box ensuring a delightful and diverse selection.")
                        return render_template("wrapgiftcat.html")
                else:
                    gift(giftid=data3.giftid, giftname=giftname, giftwrapqual=wrapqual, giftprice=amount,
                         wrapcharges=wrapcharges, recpname=name, giftmess=mess).save()
            else:
                gift(giftid=gift_id, giftname=giftname, giftwrapqual=wrapqual, giftprice=amount,
                     wrapcharges=wrapcharges, recpname=name, giftmess=mess).save()
            giftitems = gift.objects()
            tamount = 0
            for i in giftitems:
                tamount += i.wrapcharges + i.giftprice
            return render_template("giftcart.html", catg="gift", giftitems=giftitems, totalamount=tamount)
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")
@app.route('/update')
def update():
    return render_template("update.html")
@app.route('/updateaction',methods=["POST"])
def updateaction():
    pname=request.form["p-name"]
    pprice=request.form["p-price"]
    x=products.objects(prod_name=pname).update(prod_price=pprice)
    return render_template("update.html")

@app.route('/adminpanel')
def adminpanel():
    return render_template("adminpanel.html")


if __name__ == '__main__':
    app.run()
