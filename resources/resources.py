from flask import jsonify,request,Response, session,make_response,render_template
from flask_restful import Resource
from database.model import user,Complaint,cart
from datetime import datetime, timedelta
from random import random
from datetime import time


class Complaint():
    def get(self):
        if session["email"] != None:
            cmp = Complaint.objects()
            return jsonify(cmp)
        else:
            return render_template("login.html")
    def post(self):
        if session["email"] != None:
            user_id = request.form.get('user_id')
            complaint_text = request.form.get('complaint_text')

            # Find the user based on the provided user ID
            use = user.objects(user_id=user_id).first()
            if not use:
                return 'User not found'

            # Create a new complaint
            complaint = Complaint(user=use, complaint_text=complaint_text)
            complaint.save()

            return 'Complaint submitted successfully'
        else:
            return render_template("login.html")

class updquantApi(Resource):
    def post(self):
        if session["email"] != None:
            print("HI in routes resources!!!")
            data = request.get_json()
            print("HI after", data)
            prodname = data.get('prodname')
            new_quantity = data.get('newQuantity')

            if prodname and new_quantity is not None:
                item_to_update = cart.objects(prodname=prodname).first()
                if item_to_update:
                    item_to_update.quantity = new_quantity
                    item_to_update.save()
                    return jsonify({"message": "Quantity updated successfully!"}), 200
                else:
                    return jsonify({"error": "Cart item not found."}), 404
            else:
                return jsonify({"error": "Bad request."}), 400
        else:
            return render_template("login.html")

class addtocart(Resource):
    def post(self,n,p):
        if session["email"] != None:
            prod_name = n
            amount = p
            timestamp = int(time.time() * 1000)
            random_num = random.randint(1000, 9999)
            cart_id = f"cart_{timestamp}_{random_num}"
            cartitem = {
                'cartid': cart_id,
                'username': session["uname"],
                'prodname': prod_name,
                'amount': amount,
                'quantity': 1
            }
            cart.objects(**cartitem).save()
            cartQuantity = cartitem['quantity']
            response = {'cartQuantity': cartQuantity}
            x = cart.objects()
            print(x)
            return make_response(render_template("card.html", cartitems=x))
        else:
            return render_template("login.html")



