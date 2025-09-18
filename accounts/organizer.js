/*
=========================================
STUDENTCONNECT ORGANIZER INTERFACE JAVASCRIPT
=========================================

This file handles all client-side functionality for organizer interfaces
including dashboard management, event creation, navigation, and 
authentication workflows.

Key Features:
- Organizer dashboard sidebar navigation
- Event management interface interactions
- Authentication modal handling
- Form validation and submission
- Professional UI interactions
- Analytics and statistics updates

Architecture:
- Component-based organization
- Event delegation for dynamic content
- Configuration-driven behavior
- Professional UX patterns
*/

document.addEventListener('DOMContentLoaded', () => {

    /*
    ===================================
    LANDING PAGE AUTHENTICATION
    ===================================
    Handle authentication modal and form switching for organizers
    accessing the platform from the landing page.
    */
    if (document.getElementById('welcome-page')) {
        // Authentication modal elements
        const authModal = document.getElementById('auth-modal');
        const signInBtn = document.getElementById('signInBtn');
        const ctaRegisterBtn = document.getElementById('cta-register-btn');
        const closeModalBtn = authModal.querySelector('.close-modal');
        
        // Form elements for switching between login and signup
        const loginForm = document.getElementById('login-form');
        const signupForm = document.getElementById('signup-form');
        const showSignupLink = document.getElementById('show-signup');
        const showLoginLink = document.getElementById('show-login');

        // Modal control functions
        const openModal = () => {
            authModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        };
        
        const closeModal = () => {
            authModal.classList.remove('active');
            document.body.style.overflow = ''; // Restore scroll
        };

        // Event listeners for modal triggers
        [signInBtn, ctaRegisterBtn].forEach(btn => {
            if (btn) {
                btn.addEventListener('click', openModal);
            }
        });
        
        // Close modal event listeners
        closeModalBtn?.addEventListener('click', closeModal);
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) closeModal();
        });

        // Form switching functionality
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

        sidebarLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                sidebarLinks.forEach(item => item.classList.remove('active'));
                link.classList.add('active');
                
                const viewId = link.dataset.view;
                dashboardViews.forEach(view => {
                    if (view.id === viewId) {
                        view.classList.remove('hidden');
                    } else {
                        view.classList.add('hidden');
                    }
                });
            });
        });

        // --- Progressive Form Logic ---
        const formSteps = document.querySelectorAll('.form-step');
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const submitBtn = document.getElementById('submitBtn');
        let currentStep = 0;

        const updateFormSteps = () => {
            formSteps.forEach((step, index) => {
                step.classList.toggle('active', index === currentStep);
            });
            prevBtn.classList.toggle('hidden', currentStep === 0);
            nextBtn.classList.toggle('hidden', currentStep === formSteps.length - 1);
            submitBtn.classList.toggle('hidden', currentStep !== formSteps.length - 1);
        };

        nextBtn.addEventListener('click', () => {
            if (currentStep < formSteps.length - 1) {
                currentStep++;
                updateFormSteps();
            }
        });
        prevBtn.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateFormSteps();
            }
        });
        updateFormSteps();

        // --- Drag & Drop Image Upload ---
        const dragDropArea = document.getElementById('drag-drop-area');
        const fileInput = document.getElementById('event-flyer');
        const imagePreview = document.getElementById('image-preview');

        dragDropArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));
        dragDropArea.addEventListener('dragover', (e) => { e.preventDefault(); dragDropArea.classList.add('active'); });
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
        
        // --- Data & State Management ---
        const dummyEvents = [
            { title: 'AI & ML Workshop', category: 'Workshop', date: '2025-08-25', status: 'Approved', registrationLink: 'https://example.com/register/ai' },
            { title: 'National Hackathon 2025', category: 'Hackathon', date: '2025-08-20', status: 'Approved', registrationLink: 'https://example.com/register/hack' },
            { title: 'Cloud Computing Summit', category: 'TechEvent', date: '2025-09-05', status: 'Pending', registrationLink: 'https://example.com/register/cloud' },
            { title: 'Internship Fair', category: 'Internship', date: '2025-07-15', status: 'Rejected', registrationLink: 'https://example.com/register/intern' },
        ];
        const eventListBody = document.getElementById('event-list-body');
        const searchInput = document.getElementById('event-search-input');

        // --- Function to update dashboard analytics ---
        function updateAnalytics() {
            const totalEvents = dummyEvents.length;
            const pendingEvents = dummyEvents.filter(event => event.status === 'Pending').length;
            const approvedEvents = dummyEvents.filter(event => event.status === 'Approved').length;

            document.getElementById('total-events-count').textContent = totalEvents;
            document.getElementById('pending-events-count').textContent = pendingEvents;
            document.getElementById('approved-events-count').textContent = approvedEvents;
        }

        // --- Renders Events Table ---
        function renderEvents(eventsToRender) {
            eventListBody.innerHTML = '';
            eventsToRender.forEach(event => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${event.title}</td>
                    <td>${event.category}</td>
                    <td>${event.date}</td>
                    <td><span class="status-badge ${event.status.toLowerCase()}">${event.status}</span></td>
                    <td>
                        <button class="action-btn" title="Edit"><i class="fas fa-edit"></i></button>
                        <button class="action-btn" title="Delete"><i class="fas fa-trash"></i></button>
                    </td>
                `;
                eventListBody.appendChild(row);
            });
        }
        
        // --- Search/Filter Logic ---
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase();
            const filteredEvents = dummyEvents.filter(event => 
                event.title.toLowerCase().includes(searchTerm)
            );
            renderEvents(filteredEvents);
        });

        // --- Handle New Event Submission ---
        document.getElementById('event-form').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const newEvent = {
                title: document.getElementById('event-title').value,
                category: document.getElementById('event-category').value,
                date: document.getElementById('event-date').value,
                status: 'Pending',
                registrationLink: document.getElementById('event-registration-link').value
            };
            
            dummyEvents.unshift(newEvent); 
            renderEvents(dummyEvents); // Re-render the full list with the new event
            updateAnalytics(); 
            
            alert('Event submitted for review successfully!');
            
            document.getElementById('event-form').reset();
            searchInput.value = ''; // Clear search field
            imagePreview.classList.add('hidden');
            currentStep = 0;
            updateFormSteps();
        });

        // --- Initial Render on Page Load ---
        renderEvents(dummyEvents);
        updateAnalytics();
    }
});