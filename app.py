from flask import Flask, render_template, request, jsonify, Response
import os, json, re, unicodedata
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
        
@app.route('/char-data-day', methods=['GET', 'POST'])
def getChartDataDate():
    # trả lại các giá trị data qua các ngày trong tháng, đã tính tổng nhé
    filePath= 'static/data/spend/spending.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding= 'utf-8') as f:
            json.dump([], f, inden=2, ensure_ascii= False)
    else: 
        try: 
            with open(filePath, 'r', encoding= 'utf-8') as f:
                df= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump([], f, inden=2, ensure_ascii= False)
    with open(filePath, 'r', encoding='utf-8') as f:
        data= json.load(f)

    total= 0
    charDay= {}
    charDayList= []
    for idx, value in enumerate(data):
        date= value[0]['date']
        if date in charDay:
            charDay[date] += int(value[0]['money'])
        else: 
            charDay[date]= int(value[0]['money'])
    charDayList.append(charDay)
    # lấy của tháng này 
    now= datetime.now()
    formatted_time= now.strftime('%Y-%m')
    charListThisMonth= []
    charDictThisMonth = {}
    # lấy tháng trong file json
    for i in charDayList:
        for idx, v in i.items():
            idxMonth= idx.split('-')[:2]
            idxMonth= '-'.join(idxMonth)
            if idxMonth==formatted_time:
                charDictThisMonth[idx] = v
    charListThisMonth.append(charDictThisMonth)
    return jsonify(charListThisMonth)


# Month chart
@app.route('/char-data-month', methods=['GET', 'POST'])
def getChartDataMonth():
    # trả lại các giá trị data qua các ngày trong tháng, đã tính tổng nhé
    filePath= 'static/data/spend/spending.json'
    os.makedirs(os.path.dirname(filePath), exist_ok= True)
    if not os.path.exists(filePath):
        with open(filePath, 'w', encoding= 'utf-8') as f:
            json.dump([], f, inden=2, ensure_ascii= False)
    else: 
        try: 
            with open(filePath, 'r', encoding= 'utf-8') as f:
                df= json.load(f)
        except json.JSONDecodeError:
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump([], f, inden=2, ensure_ascii= False)
    with open(filePath, 'r', encoding='utf-8') as f:
        data= json.load(f)
    # Lấy năm: 
    now= datetime.now()
    monthDict= {}
    monthList= []
    for i in data: 
        month= i[0]['date']
        strfMonth= month.split('-')[:2]
        strfMonth= '-'.join(strfMonth)
        if strfMonth in monthDict:
            monthDict[strfMonth] += int(i[0]['money'])
        if strfMonth not in monthDict: 
            monthDict[strfMonth] = int(i[0]['money'])
    monthList.append(monthDict)
    return jsonify(monthList)
    
catalog= ['ăn', 'uống', 'nhà', 'dịch vụ','mua', 'khác']
def strip_accents(s: str) -> str:
    # remove diacritics
    return ''.join(ch for ch in unicodedata.normalize('NFD', s)
                   if unicodedata.category(ch) != 'Mn')

@app.route('/char-data-catalog', methods=['GET', 'POST'])
def getChartDataCatalog():
    filePath = 'static/data/spend/spending.json'
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Init result
    cat_totals = {k: 0 for k in catalog}

    norm_catalog = [strip_accents(k).lower() for k in catalog]

    # Tháng và năm hiện tại
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    for row in data:
        item = row[0]
        title = strip_accents(str(item.get('title', ''))).lower()
        money = int(item.get('money', 0))

        # Parse ngày
        try:
            date_obj = datetime.strptime(item.get('date', ''), "%Y-%m-%d")
        except ValueError:
            continue  # bỏ qua nếu date sai format

        # Chỉ tính cho tháng & năm hiện tại
        if date_obj.month != current_month or date_obj.year != current_year:
            continue

        tokens = set(re.findall(r'\w+', title))

        matched = False
        for raw_key, norm_key in zip(catalog, norm_catalog):
            if norm_key in tokens:
                cat_totals[raw_key] += money
                matched = True
                break

        if not matched:
            cat_totals["khác"] += money

    return Response(json.dumps([cat_totals], ensure_ascii=False),
                    mimetype='application/json')

@app.route('/spend-trans', methods=['GET', 'POST'])
def spendTrans():
    filePath = 'static/data/spend/spending.json'
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    # Safe load
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # return data 
    return Response(json.dumps(data, ensure_ascii= False), 
                    mimetype= 'application/json')


if __name__== '__main__':
    app.run(debug=True)