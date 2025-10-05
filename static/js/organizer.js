document.addEventListener('DOMContentLoaded', () => {
    try {
        console.log('Dashboard JavaScript loaded successfully');

        // Auto-refresh configuration
        window.dashboardConfig = {
            autoRefresh: {
                enabled: true,
                interval: 10000, // 10 seconds
                enableIndicator: true,
                pauseOnInteraction: true
            }
        };

    // --- LOGIC FOR LOGIN/LANDING PAGE ---
    if (document.getElementById('welcome-page')) {
        const authModal = document.getElementById('auth-modal');
        const openModalBtns = [document.getElementById('signInBtn'), document.getElementById('cta-register-btn')];
        const closeModalBtn = authModal.querySelector('.close-modal');
        const loginForm = document.getElementById('login-form');
        const signupForm = document.getElementById('signup-form');
        const showSignupLink = document.getElementById('show-signup');
        const showLoginLink = document.getElementById('show-login');


        const openModal = () => authModal.classList.add('active');
        const closeModal = () => authModal.classList.remove('active');

        openModalBtns.forEach(btn => btn?.addEventListener('click', openModal));
        closeModalBtn?.addEventListener('click', closeModal);
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) closeModal();
        });

        showSignupLink?.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.classList.add('hidden');
            signupForm.classList.remove('hidden');
        });

        showLoginLink?.addEventListener('click', (e) => {
            e.preventDefault();
            signupForm.classList.add('hidden');
            loginForm.classList.remove('hidden');
        });

        
        // const handleAuthSuccess = (e) => {
        //     e.preventDefault();
        //     window.location.href = 'organizer-dashboard.html';
        // };

        // loginForm?.addEventListener('submit', handleAuthSuccess);
        // signupForm?.addEventListener('submit', handleAuthSuccess);
    }


    // --- LOGIC FOR DASHBOARD PAGE ---
    if (document.getElementById('dashboard-page')) {
        // --- Dashboard View Navigation ---
        const sidebarLinks = document.querySelectorAll('.sidebar-nav li');
        const dashboardViews = document.querySelectorAll('.dashboard-view');

        // Global showView function for template usage
        window.showView = function(viewId) {
            // Remove active class from all sidebar links
            sidebarLinks.forEach(item => item.classList.remove('active'));
            
            // Add active class to the matching sidebar link
            const matchingLink = document.querySelector(`[data-view="${viewId}"]`);
            if (matchingLink) {
                matchingLink.classList.add('active');
            }
            
            // Hide all views and show the target view
            dashboardViews.forEach(view => {
                if (view.id === viewId) {
                    view.classList.remove('hidden');
                } else {
                    view.classList.add('hidden');
                }
            });
        };

        sidebarLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const viewId = link.dataset.view;
                if (viewId) {
                    // Only prevent default for internal view navigation
                    e.preventDefault();
                    showView(viewId);
                }
                // Allow normal navigation for external links (like About)
            });
        });

        // Check localStorage for navigation from edit page
        if (localStorage.getItem('showCreateEvent') === 'true') {
            showView('create-event-view');
            localStorage.removeItem('showCreateEvent');
        } else if (localStorage.getItem('showProfile') === 'true') {
            showView('profile-page');
            localStorage.removeItem('showProfile');
        } else {
            // Ensure default dashboard view is shown
            showView('dashboard-overview');
        }

        // --- Progressive Form Logic ---
        const formSteps = document.querySelectorAll('.form-step');
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const submitBtn = document.getElementById('submitBtn');
        let currentStep = 0;

        const updateFormSteps = () => {
            if (formSteps.length === 0) return; // Guard against missing form steps
            
            formSteps.forEach((step, index) => {
                step.classList.toggle('active', index === currentStep);
            });
            
            if (prevBtn) prevBtn.classList.toggle('hidden', currentStep === 0);
            if (nextBtn) nextBtn.classList.toggle('hidden', currentStep === formSteps.length - 1);
            if (submitBtn) submitBtn.classList.toggle('hidden', currentStep !== formSteps.length - 1);
        };

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                if (currentStep < formSteps.length - 1) {
                    currentStep++;
                    updateFormSteps();
                }
            });
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentStep > 0) {
                    currentStep--;
                    updateFormSteps();
                }
            });
        }
        
        // Initialize form steps
        updateFormSteps();
        
        // --- Date Validation ---
        const dateInput = document.getElementById('event-date');
        if (dateInput) {
            // Set minimum date to today
            const today = new Date().toISOString().split('T')[0];
            dateInput.setAttribute('min', today);
            
            dateInput.addEventListener('change', function() {
                const selectedDate = new Date(this.value);
                const currentDate = new Date();
                
                if (selectedDate < currentDate) {
                    alert('Event date cannot be in the past.');
                    this.value = today;
                }
            });
        }

        // --- Drag & Drop Image Upload ---
        const dragDropArea = document.getElementById('drag-drop-area');
        const fileInput = document.getElementById('event-flyer');
        const imagePreview = document.getElementById('image-preview');

        if (dragDropArea && fileInput && imagePreview) {
            dragDropArea.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));
            dragDropArea.addEventListener('dragover', (e) => { 
                e.preventDefault(); 
                dragDropArea.classList.add('active'); 
            });
            dragDropArea.addEventListener('dragleave', () => dragDropArea.classList.remove('active'));
            dragDropArea.addEventListener('drop', (e) => {
                e.preventDefault();
                dragDropArea.classList.remove('active');
                handleFile(e.dataTransfer.files[0]);
            });

            function handleFile(file) {
                if (file && file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        imagePreview.src = e.target.result;
                        imagePreview.classList.remove('hidden');
                    };
                    reader.readAsDataURL(file);
                }
            }
        }
        
        // --- Data & State Management ---
        // Note: Events are now rendered server-side in the template
        // JavaScript only handles search functionality
        const eventListBody = document.getElementById('active-event-list-body');
        const searchInput = document.getElementById('event-search-input');

        // Get events from DOM to work with search
        function getEventsFromDOM() {
            if (!eventListBody) return [];
            
            const rows = eventListBody.querySelectorAll('tr');
            const events = [];
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 4) {
                    events.push({
                        title: cells[0].textContent.trim(),
                        category: cells[1].textContent.trim(),
                        date: cells[2].textContent.trim(),
                        status: cells[3].textContent.trim(),
                        row: row
                    });
                }
            });
            return events;
        }

        // --- Function to update dashboard analytics ---
        function updateAnalytics() {
            const events = getEventsFromDOM();
            const totalEvents = events.length;
            const pendingEvents = events.filter(event => event.status.toLowerCase().includes('pending')).length;
            const approvedEvents = events.filter(event => event.status.toLowerCase().includes('approved')).length;

            const totalCountEl = document.getElementById('total-events-count');
            const pendingCountEl = document.getElementById('pending-events-count');
            const approvedCountEl = document.getElementById('approved-events-count');

            if (totalCountEl) totalCountEl.textContent = totalEvents;
            if (pendingCountEl) pendingCountEl.textContent = pendingEvents;
            if (approvedCountEl) approvedCountEl.textContent = approvedEvents;
        }

        // --- Search/Filter Logic ---
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                const searchTerm = searchInput.value.toLowerCase();
                const events = getEventsFromDOM();
                
                events.forEach(event => {
                    if (event.title.toLowerCase().includes(searchTerm)) {
                        event.row.style.display = '';
                    } else {
                        event.row.style.display = 'none';
                    }
                });
            });
        }

        // --- Handle New Event Submission ---
        const eventForm = document.getElementById('event-form');
        if (eventForm) {
            eventForm.addEventListener('submit', (e) => {
                // Validate required fields before submission
                const requiredFields = eventForm.querySelectorAll('[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        field.style.borderColor = '#dc3545';
                        isValid = false;
                    } else {
                        field.style.borderColor = '#28a745';
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    alert('Please fill in all required fields.');
                    return;
                }
                
                // Show loading state
                const submitBtn = document.getElementById('submitBtn');
                if (submitBtn) {
                    submitBtn.textContent = 'Submitting...';
                    submitBtn.disabled = true;
                }
            });
        }

        // --- Initial Page Load ---
        // Note: Analytics counts are provided by Django template, no need to override
        
        // --- Profile Image Upload ---
        const profileUploadInput = document.getElementById('profile-upload-input');
        const profilePicturePreview = document.getElementById('profile-picture-preview');
        const uploadBtn = document.querySelector('.upload-btn');
        
        if (profileUploadInput && profilePicturePreview) {
            profileUploadInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file && file.type.startsWith('image/')) {
                    // Show loading state
                    if (uploadBtn) {
                        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                    }
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        profilePicturePreview.src = e.target.result;
                        // Reset button text
                        if (uploadBtn) {
                            uploadBtn.innerHTML = '<i class="fas fa-camera"></i> Upload Photo';
                        }
                    };
                    reader.readAsDataURL(file);
                } else if (file) {
                    alert('Please select a valid image file.');
                    profileUploadInput.value = '';
                }
            });
        }
        
        // --- Profile Form Submission ---
        const profileForm = document.getElementById('profile-form');
        if (profileForm) {
            profileForm.addEventListener('submit', function(e) {
                const formData = new FormData(this);
                const hasFile = formData.get('avatar') && formData.get('avatar').size > 0;
                
                if (hasFile) {
                    console.log('Uploading avatar:', formData.get('avatar').name);
                } else {
                    console.log('No avatar file selected');
                }
                
                const saveBtn = document.getElementById('save-profile-btn');
                if (saveBtn) {
                    saveBtn.textContent = 'Saving...';
                    saveBtn.disabled = true;
                }
            });
        }
    }
    
    } catch (error) {
        console.error('Dashboard JavaScript Error:', error);
    }
});

// Global logout confirmation function
function confirmLogout() {
    if (confirm('Are you sure you want to logout?')) {
        const logoutForm = document.getElementById('logout-form');
        if (logoutForm) {
            logoutForm.submit();
        }
    }
}