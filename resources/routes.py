from .resources import updquantApi, addtocart
def initialize_routes(api):
    api.add_resource(updquantApi, '/api/update_quantity')
    api.add_resource(addtocart, '/api/add_to_cart/<n>/<p>')
