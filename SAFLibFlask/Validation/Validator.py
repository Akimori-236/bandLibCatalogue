import functools
from flask import Flask, jsonify, render_template, request, g
from werkzeug.datastructures import Authorization
from config.settings import Settings
import re



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