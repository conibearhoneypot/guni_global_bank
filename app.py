import hashlib
import socket
import requests
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

admin_username = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
admin_password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

class GetIPv4Info:
    __slots__ = "ip"

    def __init__(self, ip:str) -> None:
        self.ip = ip

    def __str__(self) -> str:
        return f"Object for {self}"
    
    def get_intruder_info(self):
        try:
            http_response = requests.get(f"https://ipinfo.io/{self.ip}/json")
            
            if http_response.status_code == 200:
                return str(http_response.json()).replace(", 'readme': 'https://ipinfo.io/missingauth'", "")
            else:
                return "Failed"
            
        except requests.RequestException:
            return "Failed"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if hashlib.sha256(username.encode('UTF-8')).hexdigest() == admin_username and hashlib.sha256(password.encode('UTF-8')).hexdigest() == admin_password:
            response = redirect(url_for("admin_dashboard"))
            return response
        else:
            return "Invalid username or password"  # Add a response for incorrect credentials

@app.route('/admin/dashboard')
def admin_dashboard():
    info = GetIPv4Info("106.213.213.236").get_intruder_info()
    ip = "106.213.213.236"

    return render_template("admin_dashboard.html", intruder_ip=ip, info=info)
