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

async function setupIndex() {
    console.log("Index page loaded");

    const form = document.getElementById('pickup-request-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const item_type = document.getElementById('item-type').value;
            const description = document.getElementById('item-desc').value;

            // Fetch the current user dynamically (replace 1 with real auth later)
            const userRes = await fetch('/api/users/1'); // Example: hardcoded user ID 1
            const userData = await userRes.json();

            // Submit pickup request with correct user_id
            const res = await fetch('/api/requests', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    item_type, 
                    item_description: description,
                    user_id: userData.id 
                })
            });

            const data = await res.json();
            document.getElementById('submission-message').innerText = data.message || "Request submitted!";
            form.reset();
        });
    }
}

function setupAdmin() {
    console.log("Admin page loaded");

    // Load Employees
    async function loadEmployees() {
        const res = await fetch('/api/employees'); 
        const employees = await res.json();
        const list = document.getElementById('employee-list');
        list.innerHTML = '';
        employees.forEach(emp => {
            const div = document.createElement('div');
            div.textContent = `${emp.name} (${emp.email}) - ${emp.phone || 'N/A'}`;
            list.appendChild(div);
        });
    }

    loadEmployees();

    // Add Employee
    const createForm = document.getElementById('create-employee-form');
    createForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('emp-name').value;
        const email = document.getElementById('emp-email').value;
        const phone = document.getElementById('emp-phone').value;

        const res = await fetch('/api/employees', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone })
        });

        const data = await res.json();
        alert(data.message || "Employee added successfully"); 
        createForm.reset();
        loadEmployees(); 
    });

    // Load Pickup Requests
    async function loadRequests() {
        const res = await fetch('/api/requests'); 
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
                <p>${req.item_description}</p>
            `;
            list.appendChild(div);
        });
    }

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
                <p>${task.item_description}</p>
            `;
            tasksList.appendChild(div);
        });
    });
}
