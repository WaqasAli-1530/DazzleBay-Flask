from .db import db
import datetime
class user(db.Document):
    username = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    phone = db.StringField(required=True)
    address = db.StringField(required=True)
class keys(db.Document):
    email = db.StringField(required=True)
    key_ = db.StringField(required=True)
class membership(db.Document):
    email = db.StringField(required=True)
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField(required=True)
    category =db.IntField(required=True)

class contact_(db.Document):
    cont_name = db.StringField(required=True)
    cont_email = db.StringField(required=True)
    cont_message = db.StringField(required=True)
class Complaint(db.Document):
    # order = db.ReferenceField(Order, required=True)
    issue_desc = db.StringField(required=True)
    status = db.StringField(required=True)
    # created_at = db.DateTimeField(default=datetime.now)
class products(db.Document):
    pic_url = db.StringField(required=True)
    category = db.StringField(required=True)
    gender = db.StringField(required=True)
    prod_name = db.StringField(required=True)
    prod_decs = db.StringField()
    prod_price = db.IntField(required=True)

class tracking(db.Document):
    quanity = db.IntField(required=True)
    price = db.IntField(required = True)
    # foreign key references to order

class cart(db.Document):
    cartid=db.StringField()
    username=db.StringField()
    prodname=db.StringField()
    quantity=db.IntField()
    amount=db.FloatField(required=True)

class gift(db.Document):
    giftid=db.StringField(required=True)
    giftname=db.StringField(required=True)
    giftwrapqual=db.StringField()
    giftprice=db.FloatField(required=True)
    wrapcharges=db.FloatField()
    recpname=db.StringField()
    giftmess=db.StringField()


