from flask import Flask, render_template, request, jsonify, Response, Blueprint
import os, json, re, unicodedata
from datetime import datetime
from invest_routes import invest_bp
from spend_routes import spend_bp

# *** Khai báo App  và blueprint***
app= Flask(__name__)
app.register_blueprint(invest_bp)
app.register_blueprint(spend_bp)
app.config['JSON_AS_ASCII'] = False 


# *** Routes start ***

# *** Routes main ***
@app.route("/", methods=['GET','POST'])
def home():
    return render_template('index.html')

# *** Routes invest tab ***
@app.route('/tab-invest-nav', methods= ['GET', 'POST'])
def navTabInvest():    
    return render_template('tab-invest.html')

# *** Routes report tab ***
@app.route('/tab-report-nav', methods= ['GET', 'POST'])
def navTabReport():    
    return render_template('tab-report.html')

if __name__== '__main__':
    app.run(debug=True)