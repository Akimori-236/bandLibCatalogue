from flask import Flask, request, jsonify, render_template
from model.Music import Music
from model.Category import Category
from flask_sqlalchemy import SQLAlchemy
from socket import gethostname

app = Flask(__name__, template_folder='templates')
app.config["DEBUG"] = True

# code from PythonAnywhere
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
username = 'elitelib22',
password = 'librarydb',
hostname = 'elitelib22.mysql.pythonanywhere-services.com',
databasename = 'elitelib22$libcatalogue',
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Front Page
@app.route('/')
@app.route("/index")
@app.route("/home")
def sanityCheck():
    return render_template("index.html", title="SAF Band Library")


# ERRORS
@app.errorhandler(500)
def error500(e):
    print(e)
    return render_template("500.html"), 500

@app.errorhandler(404)
def error404(e):
    print(e)
    return render_template("404.html"), 404

###########################################

# GET all Music
@app.route('/music')    # GET method by default
def getAllSheetmusic():
    try:
        jsonSheetmusic = Music.getAllMusic()
        output = {"Music": jsonSheetmusic}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# GET one music by provided musicID
@app.route('/music/<int:musicid>')   # GET method by default
def getOneMusic(musicid):
    try:
        jsonMusic = Music.getMusicById(musicid)

        if len(jsonMusic)>0:
            output = {"Music": jsonMusic}
            return jsonify(output), 200     # OK
        else:
            output = {}
            return jsonify(output), 404     # Not found
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# INSERT new music
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


#DELETE music with specified musicid
@app.route('/music/<int:musicid>',methods=['DELETE'])
def deleteMusic(musicid):
    try:
        rows = Music.deleteMusic(musicid)
        output = {"Rows Affected": rows}
        return jsonify(output), 200
    except Exception as err:
        print(err)
        return {}, 500


# SEARCH music by substring
@app.route('/search/music',methods=['GET'])
def getMusicBySubstring():
    try:
        substring = request.args['substring']   # will be request.form for POST method
        music = Music.getMusicBySubstring(substring)
        if len(music) > 0:
            output = {"Music": music}
            return jsonify(output), 200      # OK
        else:
            output = {}
            return jsonify(output), 404      # Not Found
    except Exception as err:
        print(err)
        return {}, 500       # Internal Server Error

####################################################

# GET all categories
@app.route('/category', methods=['GET'])
def getAllCategory():
    try:
        jsonCategory = Category.getAllCategory()
        output = {"Categories": jsonCategory}
        return jsonify(output), 200     # OK
    except Exception as err:
        print(err)
        return {}, 500      # internal server error


# INSERT new category
@app.route('/category', methods=['POST'])
def insertCategory():
    try:
        jsonCategory = request.json
        rows = Category.insertCategory(jsonCategory)
        output = {"Categories Inserted": rows}
        return jsonify(output), 201     # Successful creation
    except Exception as err:
        print(err)
        return {},500



if __name__ == "__main__":
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run(debug=True)
        # app.run(port=8000, debug=True) to run in port 8000