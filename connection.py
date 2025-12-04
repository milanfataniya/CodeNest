from flask import Blueprint
import mysql.connector as mycon
connection_bp=Blueprint("conection",__name__)

@connection_bp.route("/connection")

def get_db_connection():
    return mycon.connect(
               host="localhost",
               user="root",
               password="",
               database="codenest")
            