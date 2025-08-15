function setActive(element, url) {
    // Xóa active cũ
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

    // Gán active cho item vừa click
    element.classList.add('active');

    // Lưu trạng thái
    localStorage.setItem('activeMenu', element.id);

    // Thêm hiệu ứng fade-out cho nội dung
    const container = document.querySelector('.container');
    if (container) {
        container.classList.add('fade-out');
        setTimeout(() => {
            window.location.href = url;
        }, 300);
    } else {
        window.location.href = url;
    }
}


// Khi load lại trang -> khôi phục trạng thái active dựa vào URL
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    let activeId = '';

    if (path === '/' || path.startsWith('/spend')) {
        activeId = 'taskbar-spend';
    } else if (path.startsWith('/tab-invest-nav') || path.startsWith('/invest')) {
        activeId = 'taskbar-invest';
    } else if (path.startsWith('/tab-report-nav') || path.startsWith('/report')) {
        activeId = 'taskbar-report';
    } else {
        // Nếu không match route nào thì dùng giá trị cũ trong localStorage
        activeId = localStorage.getItem('activeMenu');
    }

    // Xóa active cũ
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

    // Gán active mới
    if (activeId) {
        const activeElement = document.getElementById(activeId);
        if (activeElement) {
            activeElement.classList.add('active');
            localStorage.setItem('activeMenu', activeId); // Cập nhật lại
        }
    }
});

document.addEventListener('DOMContentLoaded', async () => {
    async function nav_taskbar(taskbarId, endPoint) {
        document.getElementById(taskbarId).addEventListener('click', async (e) => {
            e.preventDefault();
            window.location.href = endPoint;
            await fetch(endPoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
        });
    }

    // Chuyển hướng tab nav
    await nav_taskbar('taskbar-spend', '/');
    await nav_taskbar('taskbar-invest', '/tab-invest-nav');
    await nav_taskbar('taskbar-report', '/tab-report-nav');
});
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    if (container) {
        container.style.opacity = 0;
        setTimeout(() => {
            container.style.opacity = 1;
        }, 50);
    }
});
