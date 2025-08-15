from flask import Flask, render_template, request, jsonify, Response, Blueprint
import os, json, re, unicodedata

invest_bp = Blueprint('invest_bp', __name__)

# invest information
@invest_bp.route('/add-invest', methods=['GET', 'POST'])
def addInvest():
    data= request.get_json()
    
    # Tạo thư mục
    filePath= 'static/data/invest/information.json'
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    # save load
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii= False)
    else: 
        try: 
            with open(filePath, 'r', encoding= 'utf-8') as f:
                inforData= json.load(f)
            if not isinstance(inforData, list):
                inforData= [inforData]
        except(FileNotFoundError, json.JSONDecodeError):
            with open(filePath, 'w', encoding= 'utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii= False)
    
    inforData.append(data)

    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(inforData, f, indent=2, ensure_ascii= False)
    
    # return data
    return Response(json.dumps(inforData, ensure_ascii= False),
                    mimetype='application/json')

@invest_bp.route('/load-investment', methods=['GET', 'POST'])
def loadInvestment():
    filePath= 'static/data/invest/information.json'

    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath): 
        with open(filePath, 'w', encoding='utf-8') as f: 
            json.dump([], f, indent=2, ensure_ascii= False)
    else: 
        try: 
            with open(filePath, 'r', encoding= 'utf-8') as f:
                data= json.load(f)
            if not isinstance(data, list):
                data= [data]
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding= 'utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii= False)
    
    return Response(json.dumps(data, ensure_ascii= False),
                    mimetype= 'application/json')


