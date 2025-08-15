let now = new Date();
let month = now.getMonth() + 1; // 1..12
let year = now.getFullYear();
let day = now.getDate(); // 1..31

// Biến hiển thị
let remainMoney = '';
let suggestSpend = '';
let remainMoneyYear='';
let suggestSpendYear= '';
const parseMoney = (s) => {
  const n = (s || '').toString().replace(/[^\d-]/g, '');
  return n ? parseInt(n, 10) : 0;
};

const formatVND = (n) => `${(n || 0).toLocaleString('vi-VN')} VNĐ`;

async function computeAndRender() {
  // Đã tiêu trong tháng
  const spentRes = await fetch('/spending/summary-month', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const spentJson = await spentRes.json();
  const spent = Object.values(spentJson[0][0])[0] || 0; // số đã tiêu (number)

  // Mục tiêu tháng
  const aimRes = await fetch('/loading-month', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const aimJson = await aimRes.json();
  const monthlyGoal = parseMoney(aimJson[1]?.value); // parse "1.500.000" -> 1500000

  const remainValue = monthlyGoal - spent;
  remainMoney = formatVND(remainValue);

  // Số ngày còn lại trong tháng
  const totalDays = new Date(year, month + 1, 0).getDate(); // last day of this month
  const remainDays = Math.max(totalDays - day, 1); // tránh chia 0

  const perDay = Math.floor(remainValue / remainDays);
  suggestSpend = formatVND(perDay);

  // mục tiêu trong năm
  const aimYear= await fetch('/loading-year', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  })
  const aimYearValue= await aimYear.json()
  const yearlyGoal= parseMoney(aimYearValue[0]?.value)

  // đã tiêu trong năm
  const spendingValueInYear= await fetch('/loading-year-total', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  })
  const spendingYearValue= await spendingValueInYear.json()
  
  // Còn lại số tiền trong năm 
  const yearlyRemain= yearlyGoal- spendingYearValue
  remainMoneyYear = formatVND(yearlyRemain);

  // suggest spend trong năm 
  const remainMonth= 12- month
  const perMonth= Math.floor(yearlyRemain / remainMonth)
  suggestSpendYear= formatVND(perMonth)

  // Render
  document.querySelector('#budgetLeftMonth').textContent = remainMoney;
  document.querySelector('#dailySuggestion').textContent = suggestSpend;
  document.querySelector('#budgetLeftYear').textContent = remainMoneyYear;
  document.querySelector('#monthlySuggestion').textContent = suggestSpendYear;
}

document.addEventListener('DOMContentLoaded', () => {
  // Định dạng input theo VND khi đổi
  const monthlyField = document.getElementById('monthlyGoal');
  monthlyField.addEventListener('change', () => {
    const val = parseMoney(monthlyField.value);
    monthlyField.value = val ? val.toLocaleString('vi-VN') : '';
  });

  document.getElementById('saveMonthly').addEventListener('click', async function () {
    const monthlyField = document.getElementById('monthlyGoal');
    const monthValue = monthlyField.value; // dạng "1.500.000"
    await fetch('/save-monthly', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify([
        { monthly: String(month) },
        { value: monthValue }
      ]),
    });

    // TÍNH LẠI sau khi lưu
    await computeAndRender();
  });

  // Yearly
  const yearlyField = document.getElementById('yearlyGoal');
  yearlyField.addEventListener('change', () => {
    const val = parseMoney(yearlyField.value);
    yearlyField.value = val ? val.toLocaleString('vi-VN') : '';
  });

  document.getElementById('saveYearly').addEventListener('click', async function () {
    const yearlyField = document.getElementById('yearlyGoal');
    const yearValue = yearlyField.value;
    await fetch('/save-year', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify([
        {
          year: String(year),
          value: yearValue
        }
      ]),
    });
  });

  document.getElementById('saveYearly').addEventListener('click', async function () {
    document.querySelector('#thisYear').textContent = year;
    let res = await fetch('/loading-year-total', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  });

  // Load giá trị input ban đầu
  (async () => {
    const mRes = await fetch('/loading-month', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const mJson = await mRes.json();
    document.getElementById('monthlyGoal').value = mJson[1]?.value || '';

    const yRes = await fetch('/loading-year', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const yJson = await yRes.json();
    document.getElementById('yearlyGoal').value = yJson[0]?.value || '';

    // Tính & hiển thị lần đầu
    await computeAndRender();
  })();
});

document.addEventListener('DOMContentLoaded', async function () {
  document.querySelector('#thisYear').textContent = year;
  let res = await fetch('/loading-year-total', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  let data = await res.json();
});

document.getElementById('addExpense').addEventListener('click', async () => {
  document.querySelector('#thisYear').textContent = year;
  let res = await fetch('/loading-year-total', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  await computeAndRender();
});
