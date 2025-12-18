/* ===================================
   UniBase - LocalStorage Management
   Storage keys and data access functions
   =================================== */

const STORAGE_KEYS = {
    USERS: 'unibase_users',
    TESTS: 'unibase_tests',
    RESULTS: 'unibase_results',
    CURRENT_USER: 'unibase_current_user'
};

// Default admin credentials
const DEFAULT_ADMIN = {
    id: 'admin-001',
    email: 'admin@unibase.com',
    password: 'admin123', // In production, this should be hashed
    role: 'admin',
    name: 'Admin User',
    createdAt: new Date().toISOString()
};

// Initialize storage with default admin
function initializeStorage() {
    if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
        const users = [DEFAULT_ADMIN];
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
    }

    if (!localStorage.getItem(STORAGE_KEYS.TESTS)) {
        localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify([]));
    }

    if (!localStorage.getItem(STORAGE_KEYS.RESULTS)) {
        localStorage.setItem(STORAGE_KEYS.RESULTS, JSON.stringify([]));
    }
}

// User management
function saveUser(user) {
    const users = getUsers();
    users.push(user);
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
}

function getUsers() {
    const users = localStorage.getItem(STORAGE_KEYS.USERS);
    return users ? JSON.parse(users) : [];
}

function getUserByEmail(email) {
    const users = getUsers();
    return users.find(user => user.email === email);
}

function setCurrentUser(user) {
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
}

function getCurrentUser() {
    const user = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
}

// Test management
function saveTest(test) {
    const tests = getTests();
    test.id = 'test-' + Date.now();
    test.createdAt = new Date().toISOString();
    tests.push(test);
    localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(tests));
    return test;
}

function getTests() {
    const tests = localStorage.getItem(STORAGE_KEYS.TESTS);
    return tests ? JSON.parse(tests) : [];
}

function getTestById(testId) {
    const tests = getTests();
    return tests.find(test => test.id === testId);
}

function updateTest(testId, updatedTest) {
    const tests = getTests();
    const index = tests.findIndex(test => test.id === testId);
    if (index !== -1) {
        tests[index] = { ...tests[index], ...updatedTest };
        localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(tests));
        return tests[index];
    }
    return null;
}

function deleteTest(testId) {
    const tests = getTests();
    const filtered = tests.filter(test => test.id !== testId);
    localStorage.setItem(STORAGE_KEYS.TESTS, JSON.stringify(filtered));
}

// Results management
function saveResult(result) {
    const results = getResults();
    result.id = 'result-' + Date.now();
    result.completedAt = new Date().toISOString();
    results.push(result);
    localStorage.setItem(STORAGE_KEYS.RESULTS, JSON.stringify(results));
    return result;
}

function getResults() {
    const results = localStorage.getItem(STORAGE_KEYS.RESULTS);
    return results ? JSON.parse(results) : [];
}

function getResultsByUserId(userId) {
    const results = getResults();
    return results.filter(result => result.userId === userId);
}

function getResultsByTestId(testId) {
    const results = getResults();
    return results.filter(result => result.testId === testId);
}

// Initialize on load
initializeStorage();
