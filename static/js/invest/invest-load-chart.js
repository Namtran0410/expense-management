document.addEventListener('DOMContentLoaded', async () => {

    let chartInstance = null;

    async function loadAndRenderChart() {
        const res = await fetch('/load-investment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await res.json();

        // Gom theo lợi nhuận/lỗ
        const grouped = {};
        data.forEach(item => {
            const profitLoss = Number(item.invest_price_now) - Number(item.invest_spend);
            grouped[item.invest_kind] = (grouped[item.invest_kind] || 0) + profitLoss;
        });

        const labels = Object.keys(grouped);
        const values = Object.values(grouped);

        // Màu cột: xanh nếu lãi, đỏ nếu lỗ
        const colors = values.map(val => val >= 0 ? '#4ade80' : '#f87171');

        const ctx = document.getElementById('investmentChart').getContext('2d');
        if (chartInstance) {
            chartInstance.destroy();
        }
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Lợi nhuận / Lỗ (VNĐ)',
                    data: values,
                    backgroundColor: colors
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const val = context.raw;
                                return val.toLocaleString('vi-VN') + ' VNĐ';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: function (value) {
                                return value.toLocaleString('vi-VN') + ' VNĐ';
                            }
                        }
                    }
                }
            }
        });
    }

    // Load lần đầu
    await loadAndRenderChart();

    // Lắng nghe sự kiện từ invest-common.js
    document.addEventListener('investmentAdded', async () => {
        await loadAndRenderChart();
    });

});
