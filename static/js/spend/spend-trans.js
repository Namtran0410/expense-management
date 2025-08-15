async function loadRecentTransactions() {
  const res = await fetch('/spend-trans', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  let data = await res.json();

  // Flatten array (vì dữ liệu dạng [ [ {..} ], [ {..} ] ... ])
  data = data.map(item => item[0]);

  // Sort theo ngày mới nhất
  data.sort((a, b) => new Date(b.date) - new Date(a.date));

  const rowsPerPage = 5;
  let currentPage = 1;
  const totalPages = Math.ceil(data.length / rowsPerPage);

  function renderTable(page) {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageData = data.slice(start, end);

    const tbody = document.querySelector("#recentTable tbody");
    tbody.innerHTML = "";

    pageData.forEach(tran => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${tran.date}</td>
        <td>${tran.title}</td>
        <td>${Number(tran.money).toLocaleString('vi-VN')}</td>
      `;
      tbody.appendChild(tr);
    });

    renderPagination();
  }

    function renderPagination() {
    const pagination = document.getElementById("recentPagination");
    pagination.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        if (i === currentPage) btn.classList.add("active");

        btn.addEventListener("click", () => {
        currentPage = i;
        renderTable(currentPage);
        });

        pagination.appendChild(btn);
    }
    }


  // Render lần đầu
  renderTable(currentPage);
}

document.addEventListener('DOMContentLoaded', loadRecentTransactions);
document.getElementById('addExpense').addEventListener('click', loadRecentTransactions)
