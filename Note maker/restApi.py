from flask_restful import Api,Resource
import sqlite3

class deleteNotes(Resource):
    def get(self,note,username):
        try:
            with sqlite3.connect("static/database/notes.db") as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM notes WHERE note = ? AND creator = ?",(note,username,))
                conn.commit()
            return {"message" : "Deleted note successfully!"}
        except Exception:
            return {"message" : Exception}
        
class editNotes(Resource):
    def get(self,note,username,newnote):
        try:
            with sqlite3.connect("static/database/notes.db") as conn:
                cur = conn.cursor()
                cur.execute("UPDATE notes SET note = ? WHERE creator = ? AND note = ?",(newnote,username,note))
                conn.commit()
            return {"message" : "Note edited successfully!"}
        except Exception:
            return {"message" : Exception}
        
class DeleteAll(Resource):
    def get(self,username):
        with sqlite3.connect("static/database/notes.db") as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM notes WHERE creator = ?",(username,))
                conn.commit()
        return {"message":f"All notes of {username} deleted successfully!"}
