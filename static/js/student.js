/*
=========================================
STUDENTCONNECT STUDENT INTERFACE JAVASCRIPT
=========================================

This file handles all client-side functionality for the student interface
including authentication, dashboard interactions, theme switching, and
responsive navigation.

Key Features:
- Auto-refresh configuration for real-time updates
- Theme switching (light/dark mode)
- Modal management for authentication
- Form validation and user feedback
- Responsive navigation handling
- Dashboard sidebar functionality
- CSRF token handling for secure AJAX requests

Architecture:
- Event-driven programming with DOM ready handlers
- Modular function organization
- Configuration objects for customizable behavior
- Cross-browser compatibility considerations
*/

/*
===================================
CSRF TOKEN UTILITIES
===================================
Helper functions for secure AJAX requests
*/

// Get CSRF token from meta tag or cookie
function getCSRFToken() {
    // Try to get from meta tag first
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
        return metaToken.getAttribute('content');
    }
    
    // Fallback to cookie method
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookieValue ? cookieValue.split('=')[1] : null;
}

// Setup CSRF headers for fetch requests
function getCSRFHeaders() {
    const token = getCSRFToken();
    return token ? {
        'X-CSRFToken': token,
        'Content-Type': 'application/x-www-form-urlencoded',
    } : {};
}

document.addEventListener('DOMContentLoaded', () => {

    /*
    ===================================
    DASHBOARD CONFIGURATION
    ===================================
    Configuration object for dashboard auto-refresh functionality.
    Enables real-time updates while respecting user interaction patterns.
    */
    window.dashboardConfig = {
        autoRefresh: {
            enabled: true,              // Enable automatic content refresh
            interval: 10000,            // Refresh every 10 seconds
            enableIndicator: true,      // Show visual refresh indicators
            pauseOnInteraction: true    // Pause during user interactions
        }
    };

    /*
    ===================================
    THEME MANAGEMENT
    ===================================
    Handle theme switching between light and dark modes.
    Persists user preference across sessions.
    */
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            // Get current theme and toggle to opposite
            const currentTheme = document.body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.body.setAttribute('data-theme', newTheme);
            
            // Could be extended to save preference to localStorage
            // localStorage.setItem('preferred-theme', newTheme);
        });
    }

    /*
    ===================================
    AUTHENTICATION MODAL MANAGEMENT
    ===================================
    Handle modal opening/closing for user authentication on landing page.
    Provides smooth UX for login/signup without page refreshes.
    */
    if (document.getElementById('welcome-page')) {
        const authModal = document.getElementById('auth-page');
        const openModalBtns = [
            document.getElementById('joinBtn'),      // Header join button
            document.getElementById('cta-join-btn')  // Hero CTA button
        ];
        const closeModalBtn = authModal.querySelector('.close-modal');

        // Modal control functions
        const openModal = () => {
            authModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        };
        
        const closeModal = () => {
            authModal.classList.remove('active');
            document.body.style.overflow = ''; // Restore scrolling
        };

        // Attach event listeners for modal triggers
        openModalBtns.forEach(btn => {
            if (btn) {
                btn.addEventListener('click', openModal);
            }
        });
        
        // Close modal event listeners
        closeModalBtn?.addEventListener('click', closeModal);
        
        // Close modal when clicking outside (on overlay)
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) {
                closeModal();
            }
        });
        
        // Close modal on Escape key press
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && authModal.classList.contains('active')) {
                closeModal();
            }
        });
    }

    /*
    ===================================
    AUTHENTICATION FORM LOGIC
    ===================================
    Handle switching between student and organizer authentication forms.
    Manages form visibility and validation for dual user types.
    */
    if (document.getElementById('auth-page')) {
        // Form toggle buttons for user type selection
        const studentToggle = document.getElementById('student-toggle');
        const organizerToggle = document.getElementById('organizer-toggle');
        const studentForms = document.getElementById('student-forms');
        const organizerForms = document.getElementById('organizer-forms');

        studentToggle.addEventListener('click', () => {
            studentToggle.classList.add('active');
            organizerToggle.classList.remove('active');
            studentForms.classList.remove('hidden');
            organizerForms.classList.add('hidden');
        });

        organizerToggle.addEventListener('click', () => {
            organizerToggle.classList.add('active');
            studentToggle.classList.remove('active');
            organizerForms.classList.remove('hidden');
            studentForms.classList.add('hidden');
            
            // Ensure organizer form fields are visible
            setTimeout(() => {
                const organizerPasswordWrappers = organizerForms.querySelectorAll('.password-wrapper');
                const organizerPasswordInputs = organizerForms.querySelectorAll('input[type="password"]');
                
                organizerPasswordWrappers.forEach(wrapper => {
                    wrapper.style.display = 'block';
                    wrapper.style.visibility = 'visible';
                });
                
                organizerPasswordInputs.forEach(input => {
                    input.style.display = 'block';
                    input.style.visibility = 'visible';
                });
                
                console.log('Organizer forms shown. Password fields:', organizerPasswordInputs.length);
            }, 100);
        });

        // --- Simplified Student Login/Signup Toggle ---
        const studentLoginForm = document.getElementById('student-login-form');
        const signupForm = document.getElementById('signup-form');
        const showSignupLink = document.getElementById('show-signup');
        const showLoginLink = document.getElementById('show-login'); // Corrected ID

        if (showSignupLink) {
            showSignupLink.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Create Account link clicked. Hiding login, showing signup.');
                if (studentLoginForm) studentLoginForm.classList.add('hidden');
                if (signupForm) signupForm.classList.remove('hidden');
            });
        } else {
            console.error('Could not find the "Create Account" link (#show-signup)');
        }

        if (showLoginLink) {
            showLoginLink.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Log In link clicked. Hiding signup, showing login.');
                if (signupForm) signupForm.classList.add('hidden');
                if (studentLoginForm) studentLoginForm.classList.remove('hidden');
            });
        } else {
            console.error('Could not find the "Log In" link (#show-login)');
        }

        // --- Organizer Login/Signup Toggle ---
        const organizerLoginForm = document.getElementById('organizer-login-form');
        const organizerSignupForm = document.getElementById('organizer-signup-form');
        const showOrganizerSignupLink = document.getElementById('show-organizer-signup');
        const showOrganizerLoginLink = document.getElementById('show-organizer-login');

        if (showOrganizerSignupLink) {
            showOrganizerSignupLink.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Create Organizer Account link clicked. Hiding login, showing signup.');
                if (organizerLoginForm) organizerLoginForm.classList.add('hidden');
                if (organizerSignupForm) organizerSignupForm.classList.remove('hidden');
            });
        } else {
            console.error('Could not find the "Create an Organizer Account" link (#show-organizer-signup)');
        }

        if (showOrganizerLoginLink) {
            showOrganizerLoginLink.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Log In link clicked. Hiding signup, showing login.');
                if (organizerSignupForm) organizerSignupForm.classList.add('hidden');
                if (organizerLoginForm) organizerLoginForm.classList.remove('hidden');
            });
        } else {
            console.error('Could not find the "Log In" link (#show-organizer-login)');
        }

        // Client-side password confirmation validation for organizer signup form
        if (organizerSignupForm) {
            organizerSignupForm.addEventListener('submit', function(e) {
                const password = document.getElementById('organizer-signup-password').value;
                const confirmPassword = document.getElementById('organizer-signup-confirm-password').value;

                if (password !== confirmPassword) {
                    e.preventDefault();
                    alert('Passwords do not match. Please check and try again.');
                    return false;
                }

                if (password.length < 8) {
                    e.preventDefault();
                    alert('Password must be at least 8 characters long.');
                    return false;
                }
            });
        }

        // Show/hide password
        const togglePasswordIcons = document.querySelectorAll('.toggle-password');
        togglePasswordIcons.forEach(icon => {
            icon.addEventListener('click', () => {
                const passwordInput = icon.previousElementSibling;
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            });
        });
    }
    
    // --- DASHBOARD PAGE LOGIC ---
    if (document.getElementById('dashboard-page')) {

        // --- Event Data with Details and Images ---
        const allEvents = [
             {
                id: "aiml-workshop-2025",
                title: "AI & ML Revolution Workshop",
                category: "workshop",
                date: "Oct 5, 2025",
                participants: "50+",
                image: "https://images.unsplash.com/photo-1620712943543-2fd617224887?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDR8fGFpfGVufDB8fHx8MTY1ODQyMjQwMw&ixlib=rb-1.2.1&q=80&w=400",
                details: {
                    description: "Dive deep into the world of Artificial Intelligence and Machine Learning. This hands-on workshop is designed for aspiring data scientists and AI enthusiasts. You'll learn the fundamentals, explore popular algorithms, and build your very own predictive model from scratch.",
                    topics: ["Intro to Python for Data Science (NumPy, Pandas)", "Supervised vs. Unsupervised Learning", "Building a Linear Regression Model", "Understanding Neural Networks", "Deploying a Simple ML Model with Flask"],
                    time: "10:00 AM - 4:00 PM IST",
                    mode: "Online (Zoom)",
                    price: "Free for students",
                    speaker: {
                        name: "Dr. Arjun Desai",
                        role: "Lead AI Scientist at TechNova",
                        avatar: "https://randomuser.me/api/portraits/men/32.jpg"
                    }
                }
            },
            {
                id: "hackathon-2025",
                title: "Innovate India Hackathon",
                category: "hackathon",
                date: "Sep 20-22, 2025",
                participants: "300+",
                image: "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDEwfHxoYWNrYXRob258ZW58MHx8fHwxNjU4NDIyMzgw&ixlib=rb-1.2.1&q=80&w=400",
                details: {
                    description: "Join India's largest student hackathon! Solve real-world problems, build innovative solutions, and network with industry experts. Prizes for top teams!",
                    topics: ["Full-stack Development", "Mobile App Development", "Data Science Challenges", "Cybersecurity", "Blockchain"],
                    time: "Starts 9:00 AM IST",
                    mode: "Hybrid (Online & Bangalore)",
                    price: "Free",
                    speaker: { name: "Ms. Priya Sharma", role: "CTO, InnovateTech", avatar: "https://randomuser.me/api/portraits/women/44.jpg" }
                }
            },
            {
                id: "intern-2025",
                title: "Frontend Developer Internship",
                category: "internship",
                date: "3-Month Role",
                participants: "15 Applicants",
                image: "https://images.unsplash.com/photo-1521737711867-e3b97375f902?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDd8fGludGVybnnoaXB8ZW58MHx8fHwxNjU4NDIyNDIz&ixlib=rb-1.2.1&q=80&w=400",
                 details: {
                    description: "Gain hands-on experience building user interfaces with a dynamic tech startup. Work with React, Vue, or Angular on real projects.",
                    topics: ["HTML/CSS/JavaScript", "React.js Ecosystem", "UI/UX Principles", "API Integration"],
                    time: "Full-time (9 AM - 5 PM)",
                    mode: "Remote",
                    price: "Paid Internship",
                    speaker: { name: "Mr. Raj Kumar", role: "Lead Frontend Engineer", avatar: "https://randomuser.me/api/portraits/men/65.jpg" }
                }
            },
            {
                id: "cloud-summit-2025",
                title: "Cloud Computing Summit",
                category: "techevent",
                date: "Nov 1, 2025",
                participants: "500+",
                image: "https://images.unsplash.com/photo-1587825140708-df876c12b44e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDEyfHxlbnwwfHx8fDE2NTg0MjI0Mzc&lib=rb-1.2.1&q=80&w=400",
                details: {
                    description: "Explore the latest trends and innovations in cloud technology. Expert speakers will cover AWS, Azure, GCP, and serverless architectures.",
                    topics: ["Serverless Computing", "Cloud Security", "DevOps on Cloud", "Containerization (Docker, Kubernetes)", "Multi-cloud Strategies"],
                    time: "9:00 AM - 6:00 PM IST",
                    mode: "Hybrid (Online & Delhi)",
                    price: "₹500 (Student Discount Available)",
                    speaker: { name: "Dr. Anya Singh", role: "Cloud Architect, GlobalTech", avatar: "https://randomuser.me/api/portraits/women/72.jpg" }
                }
            }
        ];

        const eventGrid = document.getElementById('event-grid');
        const allPageSections = document.querySelectorAll('.page-content');
        const discoverPage = document.getElementById('discover-page');
        const detailsPage = document.getElementById('event-details-page');

        // DISABLED: This function was overriding server-side rendered events
        // const renderEvents = (eventsToRender) => {
        //     if (!eventGrid) return;
        //     eventGrid.innerHTML = '';
        //     if (eventsToRender.length === 0) {
        //          eventGrid.innerHTML = `<p>No events found matching your criteria.</p>`;
        //          return;
        //     }
        //     eventsToRender.forEach(event => {
        //         const card = `
        //             <div class="event-card">
        //                 <img src="${event.image}" alt="${event.title}" class="event-card-image">
        //                 <div class="event-card-content">
        //                     <div class="event-card-header">
        //                         <span class="event-card-tag">${event.category}</span>
        //                         <button class="bookmark-btn"><i class="far fa-bookmark"></i></button>
        //                     </div>
        //                     <h3>${event.title}</h3>
        //                     <p class="event-card-info"><i class="fas fa-calendar-alt"></i> ${event.date}</p>
        //                     <div class="event-card-footer">
        //                         <span class="participants"><i class="fas fa-users"></i> ${event.participants}</span>
        //                         <button class="view-details-btn" data-event-id="${event.id}">View Details</button>
        //                     </div>
        //                 </div>
        //             </div>
        //         `;
        //         eventGrid.innerHTML += card;
        //     });
        // };

        document.querySelectorAll('.sidebar-nav li').forEach(link => {
            link.addEventListener('click', (e) => {
                const pageId = link.dataset.page;
                if (pageId) {
                    // Only prevent default for internal page navigation
                    e.preventDefault();
                    document.querySelectorAll('.sidebar-nav li').forEach(item => item.classList.remove('active'));
                    link.classList.add('active');
                    const pageElement = document.getElementById(pageId + "-page");
                    if (pageElement) showPage(pageElement);
                }
                // Allow normal navigation for external links (like About)
            });
        });

        const showPage = (pageToShow) => {
            allPageSections.forEach(page => page.classList.add('hidden'));
            pageToShow.classList.remove('hidden');
        };

        const showEventDetails = (eventId) => {
            const event = allEvents.find(e => e.id === eventId);
            if (!event || !event.details) {
                alert("Details for this event are not available yet.");
                return;
            }
            
            document.getElementById('details-title').textContent = event.title;
            document.getElementById('details-description').textContent = event.details.description;
            document.getElementById('details-date').innerHTML = `<strong>Date:</strong> ${event.date}`;
            document.getElementById('details-time').innerHTML = `<strong>Time:</strong> ${event.details.time}`;
            document.getElementById('details-mode').innerHTML = `<strong>Mode:</strong> ${event.details.mode}`;
            document.getElementById('details-price').textContent = event.details.price;
            document.getElementById('details-speaker-name').textContent = event.details.speaker.name;
            document.getElementById('details-speaker-role').textContent = event.details.speaker.role;
            document.getElementById('details-speaker-avatar').src = event.details.speaker.avatar;
            
            const topicsList = document.getElementById('details-topics');
            topicsList.innerHTML = '';
            event.details.topics.forEach(topic => {
                topicsList.innerHTML += `<li>${topic}</li>`;
            });
            
            showPage(detailsPage);
        };
        
        if (eventGrid) {
            eventGrid.addEventListener('click', (e) => {
                if (e.target && e.target.matches('.view-details-btn')) {
                    const eventId = e.target.dataset.eventId;
                    showEventDetails(eventId);
                }
            });
        }
        
        document.getElementById('back-to-discover').addEventListener('click', () => {
            showPage(discoverPage);
        });

        // document.querySelectorAll('.sidebar-nav li').forEach(link => {
        //     link.addEventListener('click', (e) => {
        //         e.preventDefault();
        //         document.querySelectorAll('.sidebar-nav li').forEach(item => item.classList.remove('active'));
        //         link.classList.add('active');
        //         const pageId = link.dataset.page + "-page";
        //         const pageElement = document.getElementById(pageId);
        //         if (pageElement) showPage(pageElement);
        //     });
        // });

        // --- Profile Page Logic ---
        const profileUploadInput = document.getElementById('profile-upload-input');
        const profilePicturePreview = document.getElementById('profile-picture-preview');

        if (profileUploadInput && profilePicturePreview) {
            profileUploadInput.addEventListener('change', () => {
                const file = profileUploadInput.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        profilePicturePreview.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }

        const saveProfileBtn = document.getElementById('save-profile-btn');

        //     saveProfileBtn.addEventListener('click', () => {
        //         const mobileNumber = document.getElementById('profile-mobile-input').value;
        //         localStorage.setItem('user_mobile', mobileNumber);

        //         const storedUser = JSON.parse(localStorage.getItem('student_user'));
        //         if (storedUser) {
        //             storedUser.mobile = mobileNumber;
        //             localStorage.setItem('student_user', JSON.stringify(storedUser));
        //         }
        //         alert('Profile updated successfully!');
        //     });
        // }

        // Get events from server-side rendered DOM
        function getEventsFromDOM() {
            const eventCards = document.querySelectorAll('.event-card');
            const events = [];
            eventCards.forEach(card => {
                const title = card.querySelector('.event-title')?.textContent.trim();
                const category = card.querySelector('.event-organizer')?.textContent.toLowerCase(); // We'll need to add category to template
                events.push({
                    title: title,
                    category: category,
                    element: card
                });
            });
            return events;
        }

        document.querySelectorAll('.filter-btn').forEach(button => {
            button.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                const category = button.dataset.category;
                
                // Filter server-side rendered events
                const eventCards = document.querySelectorAll('.event-card');
                eventCards.forEach(card => {
                    if (category === 'all') {
                        card.style.display = 'block';
                    } else {
                        const eventCategory = card.getAttribute('data-category');
                        if (eventCategory === category) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        });

        const searchBar = document.getElementById('search-bar');
        if (searchBar) {
            searchBar.addEventListener('keyup', (e) => {
                const searchTerm = e.target.value.toLowerCase();
                
                // Search server-side rendered events
                const eventCards = document.querySelectorAll('.event-card');
                eventCards.forEach(card => {
                    const title = card.querySelector('.event-title')?.textContent.toLowerCase() || '';
                    const organizer = card.querySelector('.event-organizer')?.textContent.toLowerCase() || '';
                    const location = card.querySelector('.event-location')?.textContent.toLowerCase() || '';
                    
                    if (title.includes(searchTerm) || organizer.includes(searchTerm) || location.includes(searchTerm)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }

        // Note: Events are now rendered server-side from Django backend
        // setTimeout(() => renderEvents(allEvents), 500); // Commented out to preserve server-side events
    }
});
