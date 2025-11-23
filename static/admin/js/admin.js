const sidebar = document.getElementById('admin-sidebar') || document.querySelector('.sidebar');
const links = Array.from(document.querySelectorAll('#admin-sidebar .nav-link'));
const currentPath = window.location.pathname;
links.forEach(a => {
try {
const hrefPath = new URL(a.href, window.location.origin).pathname;
if (hrefPath === currentPath) a.classList.add('active');
} catch (e) {  }
});



const toggleIds = ['sidebarCollapseBtn','sidebarToggle','sidebarToggleLg','sidebarToggleBtn'];
toggleIds.forEach(id => {
const btn = document.getElementById(id);
if (!btn) return;
btn.addEventListener('click', () => {
const sb = document.getElementById('admin-sidebar') || document.querySelector('.sidebar');
if (!sb) return;
const collapsed = sb.classList.toggle('collapsed');
btn.setAttribute('aria-expanded', (!collapsed).toString());
if (window.innerWidth < 992) {
if (!sb.classList.contains('collapsed')) { document.body.style.overflow = 'hidden'; }
else { document.body.style.overflow = ''; }
}
});
});



document.addEventListener('click', (e) => {
const sb = document.getElementById('admin-sidebar') || document.querySelector('.sidebar');
if (!sb) return;
if (window.innerWidth >= 992) return; 
if (!sb.classList.contains('collapsed')) {
const toggle = document.getElementById('sidebarToggle') || document.getElementById('sidebarCollapseBtn');
if (toggle && (e.target === sb || sb.contains(e.target))) return; 
if (toggle && (e.target === toggle || toggle.contains(e.target))) return; 

sb.classList.add('collapsed');
document.body.style.overflow = '';
}
});



document.querySelectorAll('[id^="sidebarToggle"]').forEach(btn => {
btn.addEventListener('keydown', (e) => {
if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); btn.click(); }
});
});
