class user():
    def __init__(self,data):
        self.cart = ""
        self.name = data['name']
        self.email = data['email']
        self.gender = data['gender']
        self.password = data["password"]
    
