import { Transform } from "../fixture/transformType.js";

async function loadInvestData() {
    const res = await fetch('/load-investment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });
    let data = await res.json();

    let investTotal = 0;
    let valueTotal = 0;
    let profitloss = 0;
    data.forEach(item => {
        investTotal += Number(item.invest_spend);
        valueTotal += Number(item.invest_price_now);
        profitloss = valueTotal - investTotal;
    });

    let t_invest = new Transform(investTotal);
    let t_value = new Transform(valueTotal);
    let t_profitLoss = new Transform(profitloss);

    document.querySelector('#totalInvested').textContent = t_invest.toThousand();
    document.querySelector('#totalCurrentValue').textContent = t_value.toThousand();

    let profitLossEl = document.querySelector('#totalProfitLoss');
    profitLossEl.textContent = t_profitLoss.toThousand();
    if (profitloss < 0) {
        profitLossEl.classList.add('loss');
        profitLossEl.classList.remove('profit');
    } else {
        profitLossEl.classList.add('profit');
        profitLossEl.classList.remove('loss');
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadInvestData();

    let investKind = '';
    let investName = '';
    let investStartDate = '';
    let investSpend = '0';
    let investPriceNow = '0';
    let investNote = '';

    document.getElementById('investment-type').addEventListener('change', e => investKind = e.target.value);
    document.getElementById('investment-name').addEventListener('change', e => investName = e.target.value);
    document.getElementById('investment-start').addEventListener('change', e => investStartDate = e.target.value);
    document.getElementById('investment-amount').addEventListener('change', e => investSpend = e.target.value);
    document.getElementById('investment-current').addEventListener('change', e => investPriceNow = e.target.value);
    document.getElementById('investment-note').addEventListener('change', e => investNote = e.target.value);

    document.getElementById('addInvestment').addEventListener('click', async () => {
        await fetch('/add-invest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                invest_kind: investKind,
                invest_name: investName,
                invest_start_date: investStartDate,
                invest_spend: investSpend,
                invest_price_now: investPriceNow,
                invest_note: investNote
            })
        });

        await loadInvestData();

        // Phát event để các file khác biết dữ liệu đã thay đổi
        document.dispatchEvent(new Event('investmentAdded'));
    });
});
