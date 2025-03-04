document.addEventListener('DOMContentLoaded', function() {
    // Mobile sidebar toggle
    const sidebarToggleBtn = document.getElementById('mobile-sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
    
    // Dark mode toggle
    const darkModeSwitch = document.getElementById('darkModeSwitch');
    
    if (darkModeSwitch) {
        darkModeSwitch.addEventListener('change', function() {
            // Update UI immediately
            document.body.classList.toggle('dark-mode');
            
            // Save preference to server
            fetch('/api/update-dark-mode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    dark_mode: this.checked
                })
            })
            .then(response => response.json())
            .then(data => console.log('Dark mode preference updated'))
            .catch(error => console.error('Error updating dark mode:', error));
        });
    }
    
    // Handle accordion persistence using localStorage
    const accordions = document.querySelectorAll('.accordion');
    
    accordions.forEach(accordion => {
        const accordionId = accordion.id;
        
        // Check if we have saved state
        const savedState = localStorage.getItem(`accordion_${accordionId}`);
        
        if (savedState) {
            try {
                const openItems = JSON.parse(savedState);
                
                // Apply saved state
                openItems.forEach(itemId => {
                    const item = document.getElementById(itemId);
                    if (item) {
                        item.classList.add('show');
                        
                        // Update the button state
                        const button = document.querySelector(`[data-bs-target="#${itemId}"]`);
                        if (button) {
                            button.classList.remove('collapsed');
                            button.setAttribute('aria-expanded', 'true');
                        }
                    }
                });
            } catch (error) {
                console.error('Error parsing accordion state:', error);
            }
        }
        
        // Listen for accordion changes
        accordion.addEventListener('shown.bs.collapse', function(event) {
            saveAccordionState(accordionId);
        });
        
        accordion.addEventListener('hidden.bs.collapse', function(event) {
            saveAccordionState(accordionId);
        });
    });
    
    function saveAccordionState(accordionId) {
        const accordion = document.getElementById(accordionId);
        if (!accordion) return;
        
        const openItems = [];
        
        accordion.querySelectorAll('.accordion-collapse.show').forEach(item => {
            openItems.push(item.id);
        });
        
        localStorage.setItem(`accordion_${accordionId}`, JSON.stringify(openItems));
    }
    
    // Handle tab persistence using localStorage
    const tabContainers = document.querySelectorAll('[role="tablist"]');
    
    tabContainers.forEach(container => {
        const containerId = container.id;
        
        // Find all tab elements
        const tabs = container.querySelectorAll('[data-bs-toggle="tab"]');
        
        // Check if we have saved state
        const savedTab = localStorage.getItem(`tab_${containerId}`);
        
        if (savedTab) {
            // Find and activate the saved tab
            tabs.forEach(tab => {
                if (tab.id === savedTab) {
                    const tabTrigger = new bootstrap.Tab(tab);
                    tabTrigger.show();
                }
            });
        }
        
        // Listen for tab changes
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', function(event) {
                localStorage.setItem(`tab_${containerId}`, event.target.id);
            });
        });
    });
});