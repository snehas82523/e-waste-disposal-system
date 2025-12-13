// Main Application 
document.addEventListener('DOMContentLoaded', () => {

    // Page Detection
    const isIndex = document.getElementById('pickup-request-form');
    const isAdmin = document.getElementById('create-employee-form');
    const isEmployee = document.getElementById('employee-select-portal');

    if (isIndex) setupIndex();
    if (isAdmin) setupAdmin();
    if (isEmployee) setupEmployeePortal();
});

function setupIndex() {
    console.log("Index page loaded");
}

function setupAdmin() {
    console.log("Admin page loaded");
}

function setupEmployeePortal() {
    console.log("Employee portal loaded");
}
