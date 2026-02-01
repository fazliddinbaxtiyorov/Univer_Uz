/* ===================================
   UniBase - Authentication System
   Handle login, registration, and session management
   =================================== */

// Registration function
function registerUser(formData) {
    const { name, email, password, confirmPassword, studentId } = formData;

    // Validation
    if (!name || !email || !password || !confirmPassword) {
        return { success: false, message: 'All fields are required' };
    }

    if (password !== confirmPassword) {
        return { success: false, message: 'Passwords do not match' };
    }

    if (password.length < 6) {
        return { success: false, message: 'Password must be at least 6 characters' };
    }

    // Check if email already exists
    const existingUser = getUserByEmail(email);
    if (existingUser) {
        return { success: false, message: 'Email already registered' };
    }

    // Create new user
    const newUser = {
        id: 'user-' + Date.now(),
        name,
        email,
        password, // In production, this should be hashed
        studentId: studentId || '',
        role: 'student',
        createdAt: new Date().toISOString()
    };

    saveUser(newUser);

    return { success: true, message: 'Registration successful!', user: newUser };
}

// Login function
function loginUser(email, password) {
    if (!email || !password) {
        return { success: false, message: 'Email and password are required' };
    }

    const user = getUserByEmail(email);

    if (!user) {
        return { success: false, message: 'Invalid email or password' };
    }

    if (user.password !== password) {
        return { success: false, message: 'Invalid email or password' };
    }

    // Set current user in session
    setCurrentUser(user);

    return { success: true, message: 'Login successful!', user };
}

// Check if user is authenticated
function isAuthenticated() {
    return getCurrentUser() !== null;
}

// Check if current user is admin
function isAdmin() {
    const user = getCurrentUser();
    return user && user.role === 'admin';
}

// Redirect based on role
function redirectToRolePage() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = 'login.html';
        return;
    }

    if (user.role === 'admin') {
        window.location.href = 'admin-dashboard.html';
    } else {
        window.location.href = 'student-dashboard.html';
    }
}

// Protect page - redirect if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

// Protect admin page - redirect if not admin
function requireAdmin() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }

    if (!isAdmin()) {
        window.location.href = 'student-dashboard.html';
    }
}

// Logout function
function handleLogout() {
    logout();
    window.location.href = 'index.html';
}

// Show/hide navigation based on auth status
function updateNavigation() {
    const user = getCurrentUser();
    const authLinks = document.getElementById('auth-links');
    const userLinks = document.getElementById('user-links');

    if (!authLinks || !userLinks) return;

    if (user) {
        authLinks.classList.add('hidden');
        userLinks.classList.remove('hidden');

        const userName = document.getElementById('user-name');
        if (userName) {
            userName.textContent = user.name;
        }
    } else {
        authLinks.classList.remove('hidden');
        userLinks.classList.add('hidden');
    }
}
