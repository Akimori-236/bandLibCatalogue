import functools
from flask import Flask, jsonify, render_template, request, g
from werkzeug.datastructures import Authorization
from config.settings import Settings
import jwt
import re

#Decorator function for APIs in app.py that needs user login and authentication
def validateJWTToken(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #do smth before
        auth = False
        auth_header = request.headers.get("Authorization")
        
        if auth_header:
            jwtToken = auth_header.split(" ")[1] #"Bearer JWTToken" the [1] selects the token itself
            print(jwtToken)
        else:
            jwtToken = None
            
        if jwtToken: #JWT string exists, check string now
            try:
                payload = jwt.decode(jwtToken, Settings.secretKey, algorithms="HS256") #decode Token with Key by Algo
                auth = True # Decoding was successful
                
                role = payload['role']
                userid = payload['userid']
                g.role = role
                g.userid = userid
            except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError) as err:
                print(err)
        
        if auth == False:
            output = {"Message": "Please log in."}
            #return jsonify(output), 400
            return render_template("notLoggedIn.html", message = output)
                
        
        value = func(*args, **kwargs)
        return value
        #do smth after   
    return wrapper


def requireAdmin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #do smth before
        admin = False
        if g.role == "admin":
            admin = True
        if not admin:
            output = {"Message": "Admin access required."}
            return jsonify(output), 400
            
        value = func(*args, **kwargs)
        return value
        #do smth after   
    return wrapper



def validateRegex(func):
    @functools.wraps(func)
    def checkRegex(*args, **kwargs):
        #do smth before
        # retrieve user input values
        name = request.json['name']
        email = request.json['email']
        role = request.json['role']
        password = request.json['password']
        
        #Construct the Regex
        patternUsername = re.compile('^[a-zA-Z0-9_]+$')
        patternEmail=re.compile('^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+@\w+\.\w+$') 
        patternPassword=re.compile('^[a-zA-Z0-9]{8,}$')
        if(patternUsername.match(name) and patternEmail.match(email) and patternPassword.match(password) and (role.lower()=="admin" or role.lower()=="member" or role.lower()=="user")):
            print("Correct")
            value = func(*args, **kwargs)
            return value

        else:
            return jsonify({"Message":"Validation Failed!"}), 403 # Validation Failed

        #do smth after
    return checkRegex