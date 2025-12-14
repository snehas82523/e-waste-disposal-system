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

    const form = document.getElementById('pickup-request-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const item_type = document.getElementById('item-type').value;
            const description = document.getElementById('item-desc').value;

            const res = await fetch('/pickup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_type, description })
            });

            const data = await res.json();
            document.getElementById('submission-message').innerText = data.message;
            form.reset();
        });
    }
}


function setupAdmin() {
    console.log("Admin page loaded");
}

function setupEmployeePortal() {
    console.log("Employee portal loaded");
}
