// Giữ instance để có thể destroy trước khi vẽ lại
let monthChartInstance = null;

async function drawMonthChart() {
  const res = await fetch('/char-data-month', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });

  const payload = await res.json();
  const dataObj = (payload && payload[0]) ? payload[0] : {};

  // Lấy label và giá trị, sắp xếp theo thời gian (YYYY-MM)
  const labels = Object.keys(dataObj).sort();       // ["2025-04","2025-06","2025-07","2025-08"]
  const values = labels.map(m => Number(dataObj[m]));

  const ctx = document.getElementById('monthChart').getContext('2d');

  // Xoá chart cũ nếu có
  if (monthChartInstance) monthChartInstance.destroy();

  monthChartInstance = new Chart(ctx, {
    type: 'bar', // đổi thành 'line' nếu bạn thích dạng đường
    data: {
      labels,
      datasets: [{
        label: 'Chi tiêu theo tháng (VNĐ)',
        data: values,
        borderWidth: 1,
        backgroundColor: 'rgba(99, 102, 241, 0.6)',
        borderColor: 'rgba(99, 102, 241, 1)'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ctx.raw.toLocaleString('vi-VN') + ' VNĐ'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            // Hiển thị dạng MM/YY cho gọn (tuỳ chọn)
            callback: (val, idx) => {
              const s = labels[idx];        // "YYYY-MM"
              const [y, m] = s.split('-');
              return `${m}/${y.slice(2)}`;  // "08/25"
            }
          },
          grid: { display: true }
        },
        y: {
          beginAtZero: true,
          ticks: {
            callback: (v) => v.toLocaleString('vi-VN')
          }
        }
      }
    }
  });
}

// Gọi khi trang load hoặc sau khi thêm chi tiêu
document.addEventListener('DOMContentLoaded', () => {
  drawMonthChart();
});

// ví dụ: sau khi bấm “Thêm” xong bạn cũng gọi lại để refresh
document.getElementById('addExpense').addEventListener('click', drawMonthChart);
