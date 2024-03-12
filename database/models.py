from .db import db
class cart(db.Document):
    cartid=db.StringField(required=True)
    username=db.StringField(required=True)
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

