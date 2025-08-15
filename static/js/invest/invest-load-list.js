document.addEventListener('DOMContentLoaded', async () => {

    function formatCurrency(value) {
        return Number(value).toLocaleString('vi-VN') + " VNĐ";
    }

    async function loadAndRenderInvestment() {
        const res = await fetch('/load-investment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await res.json();

        const tbody = document.querySelector("#investmentTable tbody");
        if (!tbody) {
            console.error("Không tìm thấy bảng #investmentTable");
            return;
        }
        tbody.innerHTML = "";

        data.forEach(item => {
            const profitLoss = Number(item.invest_price_now) - Number(item.invest_spend);
            const row = `
                <tr>
                    <td>${item.invest_kind}</td>
                    <td>${item.invest_name}</td>
                    <td>${item.invest_start_date}</td>
                    <td>${formatCurrency(item.invest_spend)}</td>
                    <td>${formatCurrency(item.invest_price_now)}</td>
                    <td style="color:${profitLoss < 0 ? 'red' : 'green'};">
                        ${formatCurrency(profitLoss)}
                    </td>
                    <td>${item.invest_note || ''}</td>
                </tr>
            `;
            tbody.insertAdjacentHTML("beforeend", row);
        });
    }

    // Load lần đầu
    await loadAndRenderInvestment();

    // Lắng nghe sự kiện từ invest-common.js
    document.addEventListener('investmentAdded', async () => {
        await loadAndRenderInvestment();
    });

});
