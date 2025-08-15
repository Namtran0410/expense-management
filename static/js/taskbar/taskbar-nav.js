function setActive(element, url) {
    // Xóa active cũ
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

    // Gán active cho item vừa click
    element.classList.add('active');

    // Chuyển trang
    window.location.href = url;

    // Lưu trạng thái vào localStorage (để khi load lại vẫn giữ màu)
    localStorage.setItem('activeMenu', element.id);
}

// Khi load lại trang -> khôi phục trạng thái active
document.addEventListener('DOMContentLoaded', () => {
    const activeId = localStorage.getItem('activeMenu');
    if (activeId) {
        const activeElement = document.getElementById(activeId);
        if (activeElement) activeElement.classList.add('active');
    }
});


document.addEventListener('DOMContentLoaded', async ()=> {
    async function nav_taskbar(taskbarId, endPoint){
        document.getElementById(taskbarId).addEventListener('click', async (e)=>{
            // e.preventDefault()
            window.location.href = endPoint;
            await fetch(endPoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
        })
    }

    // Chuyển hướng tab nav
    await nav_taskbar('taskbar-spend', '/')
    await nav_taskbar('taskbar-invest', '/tab-invest-nav')
    await nav_taskbar('taskbar-report', '/tab-report-nav')
    
})
