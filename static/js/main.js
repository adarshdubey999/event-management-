// Smart Event Management System - JavaScript Utilities

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss Bootstrap flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirmation helper for deleting events
function confirmDelete(eventTitle) {
    return confirm(`Are you sure you want to delete the event: "${eventTitle}"? This will also remove all its student registrations.`);
}

// Confirmation helper for cancelling registration
function confirmCancel(eventTitle) {
    return confirm(`Are you sure you want to cancel your registration for: "${eventTitle}"?`);
}

// Demo Credentials Autofill for examiner presentation
function fillDemo(role) {
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');

    if (!emailField || !passwordField) return;

    if (role === 'admin') {
        emailField.value = 'admin@college.edu';
        passwordField.value = 'Admin@123';
    } else if (role === 'student') {
        emailField.value = 'student@college.edu';
        passwordField.value = 'Student@123';
    }
}
