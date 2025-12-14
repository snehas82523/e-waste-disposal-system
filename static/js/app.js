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

    // Load Employees
    async function loadEmployees() {
        const res = await fetch('/employees'); 
        const employees = await res.json();
        const list = document.getElementById('employee-list');
        list.innerHTML = '';
        employees.forEach(emp => {
            const div = document.createElement('div');
            div.textContent = `${emp.name} (${emp.email}) - ${emp.phone || 'N/A'}`;
            list.appendChild(div);
        });
    }

    // Initial load
    loadEmployees();

    // Add Employee
    const createForm = document.getElementById('create-employee-form');
    createForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('emp-name').value;
        const email = document.getElementById('emp-email').value;
        const phone = document.getElementById('emp-phone').value;

        const res = await fetch('/employees', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone })
        });

        const data = await res.json();
        alert(data.message); 
        createForm.reset();
        // Refresh employee list
    });
        loadEmployees(); 

    // Load Pickup Requests
    async function loadRequests() {
        // GET all pickup requests
        const res = await fetch('/pickup'); 
        const requests = await res.json();
        const list = document.getElementById('request-list');
        list.innerHTML = '';

        requests.forEach(req => {
            const div = document.createElement('div');
            div.classList.add('request-card');
            div.innerHTML = `
                <div class="req-header">
                    <span class="req-id">#${req.id} - ${req.item_type}</span>
                    <span class="badge badge-pending">${req.status}</span>
                </div>
                <p>${req.description}</p>
            `;
            list.appendChild(div);
        });
    }

    // Initial load of pickup requests
    loadRequests();
}

function setupEmployeePortal() {
    console.log("Employee portal loaded");

    const select = document.getElementById('employee-select-portal');
    const tasksList = document.getElementById('my-tasks-list');

    select.addEventListener('change', async () => {
        const empId = select.value;
        if (!empId) return;

        const res = await fetch(`/employee/${empId}/tasks`);
        const tasks = await res.json();

        tasksList.innerHTML = '';
        if (tasks.length === 0) {
            tasksList.innerHTML = '<p>No active tasks assigned.</p>';
            return;
        }

        tasks.forEach(task => {
            const div = document.createElement('div');
            div.classList.add('request-card');
            div.innerHTML = `
                <div class="req-header">
                    <span class="req-id">#${task.id} - ${task.item_type}</span>
                    <span class="badge badge-info">${task.status}</span>
                </div>
                <p>${task.description}</p>
            `;
            tasksList.appendChild(div);
        });
    });
}
