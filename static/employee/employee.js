
document.addEventListener('DOMContentLoaded', function() {
    const links = Array.from(document.querySelectorAll('.sidebar-emp .nav-link'));
    const currentPath = window.location.pathname;

    links.forEach(a => {
        try 
        {
            const hrefPath = new URL(a.href, window.location.origin).pathname;
            if (hrefPath === currentPath)
            {
                a.classList.add('active');
            }
        }
        catch (e) {}
    });
});