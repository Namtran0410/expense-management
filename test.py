data= [
  [
    {
      "title": "Ăn sáng",
      "date": "2025-08-13",
      "money": "50000"
    }
  ],
  [
    {
      "title": "Ăn sáng",
      "date": "2025-08-12",
      "money": "50000"
    }
  ],
  [
    {
      "title": "Ăn sáng",
      "date": "2025-08-11",
      "money": "50000"
    }
  ],
  [
    {
      "title": "Ăn trưa",
      "date": "2025-06-10",
      "money": "150000"
    }
  ],
  [
    {
      "title": "Ăn cưới",
      "date": "2025-07-17",
      "money": "500000"
    }
  ],
  [
    {
      "title": "Ăn Nhậu",
      "date": "2025-06-11",
      "money": "700000"
    }
  ],
  [
    {
      "title": "Mua áo",
      "date": "2025-06-18",
      "money": "500000"
    }
  ],
  [
    {
      "title": "Mua áo",
      "date": "2025-06-18",
      "money": "500000"
    }
  ],
  [
    {
      "title": "Mua áo",
      "date": "2025-06-18",
      "money": "500000"
    }
  ],
  [
    {
      "title": "Mua quần",
      "date": "2025-06-10",
      "money": "250000"
    }
  ],
  [
    {
      "title": "Mua đồ ",
      "date": "2025-04-13",
      "money": "500000"
    }
  ],
  [
    {
      "title": "mua sách",
      "date": "2025-08-01",
      "money": "250000"
    }
  ],
  [
    {
      "title": "Ăn đêm",
      "date": "2025-08-14",
      "money": "50000"
    }
  ],
  [
    {
      "title": "Ăn tối ",
      "date": "2025-08-01",
      "money": "30000"
    }
  ],
  [
    {
      "title": "Ăn tối ",
      "date": "2025-08-01",
      "money": "30000"
    }
  ],
  [
    {
      "title": "ăn tối",
      "date": "2025-08-01",
      "money": "30000"
    }
  ],
  [
    {
      "title": "ăn tối",
      "date": "2025-08-01",
      "money": "30000"
    }
  ],
  [
    {
      "title": "ăn tối",
      "date": "2025-08-01",
      "money": "30000"
    }
  ],
  [
    {
      "title": "ăn tối",
      "date": "2025-08-01",
      "money": "50000"
    }
  ],
  [
    {
      "title": "Ăn vặt trà sữa",
      "date": "2025-08-01",
      "money": "50000"
    }
  ],
  [
    {
      "title": "Nhà ở ",
      "date": "2025-08-05",
      "money": "5000000"
    }
  ],
  [
    {
      "title": "Tiền nhà",
      "date": "2025-07-05",
      "money": "5000000"
    }
  ],
  [
    {
      "title": "Tiền dịch vụ",
      "date": "2025-07-05",
      "money": "1250000"
    }
  ],
  [
    {
      "title": "Tiền dịch vụ",
      "date": "2025-08-05",
      "money": "1250000"
    }
  ],
  [
    {
      "title": "uống trà",
      "date": "2025-08-14",
      "money": "35000"
    }
  ],
  [
    {
      "title": "uống trà",
      "date": "2025-08-15",
      "money": "35000"
    }
  ]
]

catalog= ['ăn', 'uống', 'nhà', 'dịch vụ', 'khác', 'điện', 'nước', 'internet']
catadict= {}
k = []
for i in data:
    title = i[0]['title']
    title= title.lower()
    titleList= title.split(' ')

    for t in titleList:
        if t in catalog:
            value= i[0]['money']
            if t in catadict:
                catadict[t] += int(value)
            if t not in catadict:
                catadict[t] = int(value)

k.append(catadict)
print(k)

