let dayChartInstance = null; // Global chart instance

// Hàm dùng để fetch dữ liệu và vẽ lại biểu đồ
async function drawDayChart() {
  const res = await fetch('/char-data-day', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });

  const charData = await res.json();
  const dataObj = charData[0];

  const labels = Object.keys(dataObj).sort();
  const values = labels.map(date => dataObj[date]);

  const ctx = document.getElementById('dayChart').getContext('2d');

  // Xoá biểu đồ cũ nếu có
  if (dayChartInstance !== null) {
    dayChartInstance.destroy();
  }

  // Vẽ biểu đồ mới
  dayChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Chi tiêu theo ngày (VNĐ)',
        data: values,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.raw.toLocaleString('vi-VN') + ' VNĐ';
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: value => value.toLocaleString('vi-VN')
          }
        }
      }
    }
  });
}

// Khi trang load lần đầu: vẽ biểu đồ luôn
document.addEventListener('DOMContentLoaded', function () {
  drawDayChart();

  // Khi bấm nút "Thêm" -> cũng vẽ lại
  document.getElementById('addExpense').addEventListener('click', function () {
    drawDayChart();
  });
});
