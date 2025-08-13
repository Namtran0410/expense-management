from flask import Flask, render_template, request, jsonify
import os, json
app= Flask(__name__)
app.config['JSON_AS_ASCII'] = False 
from datetime import datetime
@app.route("/")
def home():
    return render_template('index.html')

# Mục tiêu tháng 
@app.route("/save-monthly", methods=['GET','POST'])
def saveMonthly():
    data= request.get_json()

    # tạo file nếu không tồn tại 
    filePath= 'static/data/month/monthValue.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent= 2, ensure_ascii= False)
    else: 
        try: 
            with open(filePath, 'r', encoding=' utf-8') as f:
                df= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump([], f, indent= 2, ensure_ascii= False)

    # ghi nội dung vào file 
    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii= False)
    return jsonify(data)
# *** Mục tiêu năm *** 
@app.route("/save-year", methods=['GET','POST'])
def saveYear():
    data= request.get_json()

    # tạo file nếu không tồn tại 
    filePath= 'static/data/year/yearValue.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)
    else: 
        try: 
            with open(filePath, 'r', encoding=' utf-8') as f:
                df= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding= 'utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii= False)
    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii= False)
    return jsonify(data)

# *** Mục tiêu tháng- load data của mỗi tháng lên ***
@app.route("/loading-month", methods= ['GET','POST'])
def loadMonth():
    # tạo file nếu không tồn tại 
    filePath= 'static/data/month/monthValue.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    # Nếu không tồn tại => tạo file và điền data rỗng
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent= 2, ensure_ascii= False)
    else: 
        # Mở nếu đúng định dạng  
        try:
            with open(filePath, 'r', encoding= 'utf-8') as f:
                data= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii= False)

    # nếu có thì return lại data đó
    return jsonify(data) 

# *** Mục tiêu tháng- Còn lại tháng này ***


# *** Mục tiêu năm - load data của năm lên  ***
@app.route("/loading-year", methods= ['GET', 'POST'])
def loadYear():
    filePath = 'static/data/year/yearValue.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    # Nếu file không tồn tại=> tạo file
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent= 2, ensure_ascii= False)
    else: 
        try:
            with open(filePath, 'r', encoding= 'utf-8') as f:
                df= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding= 'utf-8') as f:
                json.dump([], f, indent= 2, ensure_ascii= False)
    return jsonify(df)

# *** Mục tiêu năm - đã chi trong năm ***
@app.route("/loading-year-total", methods=['GET', 'POST'])
def loadingYearTotal():
    # Tạo file chứa data
    filePath= 'static/data/spend/spending.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath): 
        with open(filePath, 'w', encoding= 'utf-8') as f:
            json.dump([], f, ensure_ascii= False, indent=2)
    else: 
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                df= json.load(f)
            if not isinstance(df, list):
                df= [df]
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump([], f, indent= 2, ensure_ascii= False)
    with open(filePath, 'r', encoding='utf-8') as f:
        df= json.load(f)

    now= datetime.now()
    formatted_time= now.strftime('%Y')
    total = 0
    for idx, value in enumerate(df):
        date= value[0]['date']
        year= str(date).split('-')[0]
        if year == formatted_time:
            total += int(value[0]['money'])
    return jsonify(total)


# *** Thêm khoản chi - lưu data ***
@app.route("/spending", methods=['GET', 'POST'])
def addSpending():
    data= request.get_json()

    # Tạo file chứa data
    filePath= 'static/data/spend/spending.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath): 
        with open(filePath, 'w', encoding= 'utf-8') as f:
            json.dump([], f, ensure_ascii= False, indent=2)
    else: 
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                df= json.load(f)
            if not isinstance(df, list):
                df= [df]
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump([], f, indent= 2, ensure_ascii= False)
    with open(filePath, 'r', encoding='utf-8') as f:
        df= json.load(f)
    if not isinstance(df, list):
        df= [df]
        
    df.append(data)
    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(df, f, ensure_ascii= False, indent=2)
    return jsonify(df)
# *** Thêm khoản chi - hôm nay ***
@app.route("/spending/summary-day", methods=['GET', 'POST'])
def calculateValue_day():
    now= datetime.now()
    formatted_time= now.strftime('%Y-%m-%d')
    filePath= 'static/data/spend/spending.json'

    # load data: 
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii= False)
    else: 
        try: 
            with open(filePath, 'r', encoding='utf-8') as f:
                df= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding= 'utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii= False)
    
    with open(filePath, 'r', encoding='utf-8') as f:
        data= json.load(f)

    total = 0
    spendList= []
    for idx, value in enumerate(data):
        if value[0]['date'] == formatted_time:
            money_int = int(value[0]['money'])
            total += money_int
    spendList.append([{formatted_time: total}])

    return jsonify(spendList)

# *** Thêm khoản chi - tháng này***
@app.route("/spending/summary-month", methods=['GET', 'POST'])
def calculateValue_month():
    now= datetime.now()
    formatted_time= now.strftime('%Y-%m-%d')
    filePath= 'static/data/spend/spending.json'

    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding= 'utf-8') as f:
            json.dump([], f, inden= 2, ensure_ascii= False)
    else: 
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                df= json.load(f)
            if not isinstance(df, list):
                df= [df]
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding= 'utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii= False )
    with open(filePath, 'r', encoding= 'utf-8') as f:
        df = json.load(f)
    
    # lọc năm và tháng
    spendList= []
    now= datetime.now()
    formatted_time= now.strftime('%Y-%m')
    total = 0 
    for idx, value in enumerate(df):
        date= str(value[0]['date'])
        dateMonth= date.split("-")[:2]
        date_Month= '-'.join(dateMonth)

        if date_Month== formatted_time:
            valueMonth= int(value[0]['money'])
            total += valueMonth
    spendList.append([{formatted_time: total}])
    return jsonify(spendList)
        


if __name__== '__main__':
    app.run(debug=True)