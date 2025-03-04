document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebarClose = document.getElementById('sidebar-close');

    // Function to close sidebar on mobile
    function closeSidebarMobile() {
        sidebar.classList.remove('expanded');
        sidebar.classList.add('collapsed');
        mainContent.classList.add('sidebar-collapsed');
    }

    // Function to toggle sidebar based on screen size
    function toggleSidebar() {
        const windowWidth = window.innerWidth;
    
        if (windowWidth > 992) {
            // For large screens, toggle between visible and collapsed
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                mainContent.classList.remove('sidebar-collapsed');
            } else {
                sidebar.classList.add('collapsed');
                mainContent.classList.add('sidebar-collapsed');
            }
        } else if (windowWidth > 768) {
            // For medium screens, toggle between icon-only and expanded
            sidebar.classList.toggle('expanded');
            mainContent.classList.toggle('sidebar-expanded');
        } else {
            // For small screens, toggle slide-in/out
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                sidebar.classList.add('expanded');
            } else {
                closeSidebarMobile();
            }
        }
    }

    menuToggle.addEventListener('click', toggleSidebar);

    // Close sidebar when clicking the close button on mobile
    sidebarClose.addEventListener('click', closeSidebarMobile);

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
        const isMobile = window.innerWidth <= 768;
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnMenuToggle = menuToggle.contains(event.target);
    
        if (isMobile && !isClickInsideSidebar && !isClickOnMenuToggle && sidebar.classList.contains('expanded')) {
            closeSidebarMobile();
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        const windowWidth = window.innerWidth;
    
        // Reset classes based on screen size
        if (windowWidth > 992) {
            sidebar.classList.remove('expanded');
            mainContent.classList.remove('sidebar-expanded');
        } else if (windowWidth <= 768) {
            closeSidebarMobile();
        }
    });
});