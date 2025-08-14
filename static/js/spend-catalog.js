// Giữ instance để có thể destroy trước khi vẽ lại
let catChartInstance = null;

async function drawCatChart() {
  const res = await fetch('/char-data-catalog', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });

  const payload = await res.json();
  const dataObj = (payload && payload[0]) ? payload[0] : {};

  const labels = Object.keys(dataObj);               // ["ăn","uống","nhà","dịch vụ","khác"]
  const values = labels.map(cat => Number(dataObj[cat]));

  const ctx = document.getElementById('catChart').getContext('2d');

  // Xoá chart cũ nếu có
  if (catChartInstance) catChartInstance.destroy();

  catChartInstance = new Chart(ctx, {
    type: 'pie', // Có thể đổi thành 'doughnut'
    data: {
      labels,
      datasets: [{
        label: 'Chi tiêu theo danh mục',
        data: values,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)'
        ],
        borderColor: '#fff',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // Cho phép co giãn theo khung
      plugins: {
        tooltip: {
          callbacks: {
            label: (ctx) => ctx.raw.toLocaleString('vi-VN') + ' VNĐ'
          }
        },
        legend: {
          position: 'right',
          labels: { boxWidth: 20 }
        }
      }
    }
  });
}

// Gọi khi trang load hoặc sau khi thêm chi tiêu
document.addEventListener('DOMContentLoaded', drawCatChart);

// Sau khi thêm khoản chi thì gọi lại để refresh
document.getElementById('addExpense').addEventListener('click', drawCatChart);
