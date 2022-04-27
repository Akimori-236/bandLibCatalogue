from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from os.path import join, dirname, realpath
from model.Music import Music
from model.User import User
# from Validation.Validator import *

app = Flask(__name__)

# home page
@app.route('/')
@app.route("/index")
@app.route("/home")
def sanityCheck():
    return render_template("index.html", title="Band Library Catalogue")
    # return "Hello World"

# ADMIN Tools
@app.route('/admin')
# @validateJWTToken
# @requireAdmin
def admin():
    return render_template("admin.html", title="Librarian Admin Tools")

# about
@app.route('/about')
def about():
    return render_template("about.html", title="Band Digitalization Team 2022", team=["ME2 Joe Tan", "ME1 Ng Wee Seng", "ME1 Vignesh", "ME1 Gerald Lim", "ME1 Kenneth Low"])

# upload csv form
@app.route('/uploadcsv')
def uploadCSV():
    return render_template("uploadcsv.html", title="Restore Database")

# # ERRORS
@app.errorhandler(500)
def error500(e):
    print(e)
    return render_template("500.html"), 500

@app.errorhandler(404)
def error404(e):
    print(e)
    return render_template("404.html"), 404


###########################################
# USERS

# Log in page
@app.route('/login')
def Login():
    return render_template("login.html", title="Librarian Login")

# # GET all users
# @app.route('/users')    # GET method by default
# @validateJWTToken
# @requireAdmin
# def getAllUsers():

#     print("g context role:"+g.role)
#     print("g context userid:"+str(g.userid))
#     try:
#         jsonUsers = User.getAllUsers()
#         output = {"Users": jsonUsers}
#         return jsonify(output), 200     # OK
#     except Exception as err:
#         print(err)
#         return {}, 500      # internal server error

# # GET one user by provided userID
# @app.route('/users/<int:userid>')   # GET method by default
# @validateJWTToken
# def getOneUser(userid):

#     print("g context role:"+g.role)
#     print("g context userid:"+str(g.userid))
#     try:
#         jsonUser = User.getUserById(userid)

#         if len(jsonUser)>0:
#             output = {"User": jsonUser}
#             return jsonify(output), 200     # OK
#         else:
#             output = {}
#             return jsonify(output), 404     # Not found
#     except Exception as err:
#         print(err)
#         return {}, 500      # internal server error

# #DELETE user with specified userid
# @app.route('/users/<int:userid>',methods=['DELETE'])
# def deleteUser(userid):
#     try:
#         rows = User.deleteUser(userid)
#         output = {"Rows Affected": rows}
#         return jsonify(output), 200
#     except Exception as err:
#         print(err)
#         return {}, 500

# # ISSUE JWTs / LOGIN
# @app.route('/users/login', methods=['POST']) # POST as token creation
# def loginUser():
#     try:
#         jsonUser = request.json
#         email = jsonUser['email']
#         password = jsonUser['password']
#         jwtToken = User.loginUser(email, password)
#         output = {"JWT": jwtToken}
#         return jsonify(output), 200     # Successful creation
#     except Exception as err:
#         print(err)
#         return {},500


# # INSERT new user
# @app.route('/users', methods=['POST'])
# @validateRegex
# def insertUser():
#     try:
#         jsonUser = request.json
#         rows = User.insertUser(jsonUser)
#         output = {"Users Inserted": rows}
#         return jsonify(output), 201     # Successful creation
#     except Exception as err:
#         print(err)
#         return {},500





###########################################

# GET all Music [keep for csv exporting for db backup]
@app.route('/music')
def getAllMusic():
    try:
        jsonMusic = Music.getAllMusic()
        output = {"Music": jsonMusic}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# # GET music by pages
# @app.route('/music',methods=['GET'])
# def getMusicByPage():
#     try:
#         page = request.args.get['page']   # will be request.form for POST method
#         musicPerPage = 10 # request.args.get('display', default='10')
#         music = Music.getMusicByPage(int(page), int(musicPerPage))

#         if len(music) > 0:
#             output = {"Music": music}
#             return jsonify(output), 200      # OK
#         else:
#             output = {}
#             return jsonify(output), 404      # Not Found
#     except Exception as err:
#         print(err)
#         return {}, 500       # Internal Server Error


# GET total number of music
@app.route('/music/totalcount',methods=['GET'])
def getTotalMusicCount():
    try:
        jsonCounter = Music.getTotalMusicCount()
        output = {"TotalMusic": jsonCounter}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# GET one music by musicID
@app.route('/music/<int:musicID>')
def getOneMusic(musicID):
    try:
        jsonMusic = Music.getMusicByID(musicID)

        if len(jsonMusic)>0:
            output = {"Music": jsonMusic}
            return jsonify(output), 200     # OK
        else:
            output = {}
            return jsonify(output), 404     # Not found
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


#DELETE music by musicID
@app.route('/music/<int:musicID>',methods=['DELETE'])
# @requireAdmin
def deleteMusicByID(musicID):
    try:
        rows = Music.deleteMusicByID(musicID)
        output = {"Rows Affected": rows}
        return jsonify(output), 200
    except Exception as err:
        print(err)
        return {}, 500


# SEARCH music by title [not working]
@app.route('/search/title',methods=['GET'])
def searchMusicByTitle():
    try:
        substring = request.args['substring']   # will be request.form for POST method
        music = Music.searchMusicByTitle(substring)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error


# INSERT new music [not tested]
@app.route('/music', methods=['POST'])
def insertMusic():
    try:
        jsonMusic = request.json
        rows = Music.insertMusic(jsonMusic)
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500


##############################################################

# Restore database by inputting a csv file
# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/uploadcsv', methods=['POST'])
def restoreDB():
    try:
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '': 
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            # save the file
            return redirect(url_for('index'))
        
        rows = Music.DBReset(uploaded_file)
        output = {"Music Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500



