from flask import Flask,render_template,request,session,redirect
import sqlite3
from datetime import datetime

def editProfile(emailid, dp):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE user_list SET dp = ? WHERE email = ?", (dp, emailid))
    conn.commit()
    conn.close()

def listDP(email):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT dp FROM user_list WHERE full_name = ?",(email,))
    dps = cursor.fetchall()
    conn.commit()
    conn.close()

    return dps

def addNotes(note,owner,date):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes(note,creator,created_date) VALUES (?,?,?)",(note,owner,date,))
    conn.commit()
    conn.close()

def viewNotes(email):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT note FROM notes WHERE creator = ?",(email,))
    notes = cursor.fetchall()
    conn.close()

    return notes

def registerUsers(users):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_list(full_name,email,password) VALUES (?,?,?)",(users[0],users[1],users[2],))
    #dp is also added
    conn.commit()
    conn.close()

def check_user_info(email_id):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM user_list WHERE email = ?", (email_id,))
    datas = cursor.fetchall()
    conn.close()

    return datas

def returnName(email_id):
    conn = sqlite3.connect("static/database/notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM user_list WHERE email = ?", (email_id,))
    datas = cursor.fetchall()
    conn.close()

    return datas
app = Flask(__name__)
app.secret_key = "SAM9644"
@app.route("/")
def home_page():
    if 'email' in session:
        return redirect("/profile")
    else:
        return render_template("home.html")


@app.route("/static/database/notes.db")
def denyAccess():
    return render_template("access_denied.html")

@app.route("/success",methods=["POST"])
def successPage():
    name,email,password = request.form.get("full-name"),request.form.get("email-id"),request.form.get("pass")
    users = [name,email,password]
    try:
        registerUsers(users=users)
        return "<script>alert('successfully registered');window.location.href='/#login';</script>'"
    except:
        return "<script>alert('Email already used!');window.location.href='/';</script>'"
    
@app.route("/profile")
def profilePage():
    if 'email' in session:
        dpic = f"static/dp/{returnName(session['email'])[0][0].replace(' ','')}.jpg"
        return render_template("profile.html",fname=returnName(session['email'])[0][0],email=session['email'],pp = dpic)
    else:
        return redirect("/")
    
@app.route("/login",methods=["POST","GET"])
def store_session():
    email,password = request.form.get("email-id2"),request.form.get("pass2")
    if (check_user_info(email_id=email)[0][0]== password):
        session['email'] = email
        session['password'] = password
        session['name'] = returnName(email)[0][0]
        return redirect("/profile")
    else:
        return "<script>alert('email or password is not correct!');window.location.href='/';</script>"

@app.route("/logout")
def endSession():
    session.clear()
    return redirect("/")

@app.route("/createnote")
def noteCreate():
    if "email" in session:
        return render_template("create_note.html")
    else:
        return "<script>alert('No login session found log in first!');window.location.href='/';</script>"
    
#saving note to database
@app.route("/savenote",methods=["POST"])
def saveNote():
    if "email" in session:
        note = request.form.get("note")
        owner = session['email']
        created_date = datetime.now()
        addNotes(note,owner,created_date)
        return "<script>alert('Note added successfully');window.location.href='/profile';</script>"
    else:
        return "<script>alert('No login session found log in first!');window.location.href='/';</script>"
    
@app.route("/viewnote")
def dispNotes():
    if "email" in session:
        notes = viewNotes(email=session['email'])
        return render_template("note_list.html",notes=notes)
    else:
        return "<script>alert('No login session found log in first!');window.location.href='/';</script>"

@app.route("/editdp")
def editPic():
    if "email" in session:
        return render_template("edit_profile.html")
    else:
        return "<script>alert('No login session found log in first!');window.location.href='/';</script>"
    
@app.route("/saveinfo",methods=["POST"])
def changeDP():
        username = returnName(email_id=session['email'])
        image = request.files['dp']
        image.save(f"static/dp/{username[0][0].replace(' ','')}.jpg")
        image_path = f"static/dp/{username[0][0].replace(' ','')}.jpg"
        editProfile(session['email'],image_path)
        return "<script>alert('Profile picture uploaded successfully!');window.location.href='/';</script>"

if __name__ == "__main__":
    app.run(debug=True)
