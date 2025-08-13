let nows = new Date();
let years = nows.getFullYear();
let months = String(nows.getMonth() + 1).padStart(2, '0');
let dates = String(nows.getDate()).padStart(2, '0');

let formatDates= `${years}-${months}-${dates}`

document.addEventListener('DOMContentLoaded', ()=> {
    const title= document.getElementById('category-spending')
    const date= document.getElementById('date-spending')
    const money= document.getElementById('amount-spending')
    const note= document.getElementById('note-spending')
    const addButton= document.getElementById('addExpense')
    let value_title
    let value_date
    let value_money
    let value_note


    // lấy các data 
    title.addEventListener('change', ()=> {
        value_title= title.value
    })
    date.addEventListener('change', ()=> {
        value_date= date.value
    })
    money.addEventListener('change', ()=> {
        value_money= money.value
    })
    note.addEventListener('change', ()=> {
        value_note= note.value
    })

    addButton.addEventListener('click', async ()=> {
        let res= await fetch('/spending', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }, 
            body: JSON.stringify([{
                title: value_title,
                date: value_date,
                money: value_money,
                note: value_note
            }])
        })

        // date 
        let resq= await fetch('/spending/summary-day', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data= await resq.json()
        const value= data[0][0][formatDates]
        document.querySelector('#todayTotal').textContent= Number(value).toLocaleString('vi-VN') + ' VNĐ'
        
        // month 
        let resw= await fetch('/spending/summary-month', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const resData= await resw.json()
        const monthYear= `${years}-${months}`
        // So sánh tháng và năm 
        const valueMonth= resData[0][0][monthYear]
        document.querySelector('#monthTotal').textContent= Number(valueMonth).toLocaleString('vi-VN') + ' VNĐ'
    })
})

// tính tổng chi tiêu của hôm nay 

document.addEventListener('DOMContentLoaded', async (e)=> {
    let res= await fetch('/spending/summary-day', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const data= await res.json()
    const value= data[0][0][formatDates]
    document.querySelector('#todayTotal').textContent= Number(value).toLocaleString('vi-VN') + ' VNĐ'
})

// tính tổng chi tiêu của tháng này
document.addEventListener('DOMContentLoaded', async ()=> {
    let resw= await fetch('/spending/summary-month', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const resData= await resw.json()
    const monthYear= `${years}-${months}`
    // So sánh tháng và năm 
    const value= resData[0][0][monthYear]
    document.querySelector('#monthTotal').textContent= Number(value).toLocaleString('vi-VN') + ' VNĐ'
    
})
