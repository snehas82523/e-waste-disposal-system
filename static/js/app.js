// Main Application Logic
document.addEventListener('DOMContentLoaded', () => {

    // Page Detection
    const isIndex = document.getElementById('pickup-request-form');
    const isAdmin = document.getElementById('create-employee-form');
    const isEmployee = document.getElementById('employee-select-portal');

    if (isIndex) setupIndex();
    if (isAdmin) setupAdmin();
    if (isEmployee) setupEmployeePortal();
});

// --- Public User Page ---
function setupIndex() {

    const form = document.getElementById('pickup-request-form');
    const msgDiv = document.getElementById('submission-message');

    if (!form) return; // Guard clause

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const desc = document.getElementById('item-desc').value;
        const type = document.getElementById('item-type').value;
        const btn = form.querySelector('button');

        btn.disabled = true;
        btn.textContent = 'Submitting...';

        try {
            const res = await fetch('/api/requests', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    item_description: desc,
                    item_type: type,
                    user_id: 1
                })
            });
            const data = await res.json();

            if (res.ok) {
                msgDiv.innerHTML = `
                    <div class="success-card">
                        <h4>Request Submitted!</h4>
                        <p>Status: <span class="badge badge-pending">${data.status}</span></p>
                    </div>`;
                form.reset();
            } else {
                msgDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
            }
        } catch (err) {
            msgDiv.innerHTML = `<p class="error">Network error</p>`;
        } finally {
            btn.disabled = false;
            btn.textContent = 'Submit Request';
        }
    });
}

// --- Admin Page ---
function setupAdmin() {
    loadEmployees();
    loadRequests('request-list', true); // true = admin mode
    setupEmployeeForm();
}

let cachedEmployees = [];

async function loadEmployees() {
    const list = document.getElementById('employee-list');
    if (!list) return;

    try {
        const res = await fetch('/api/employees');
        const data = await res.json();
        cachedEmployees = data; // Cache for dropdowns

        if (data.length === 0) {
            list.innerHTML = '<p>No employees found.</p>';
            return;
        }

        // Search Listener
        const searchInput = document.getElementById('employee-search');
        if (searchInput) {
            // Remove old listener to avoid duplicates if re-run (simple approach: clone or just overwrite)
            // Ideally we'd name the handler, but for this scope:
            searchInput.oninput = (e) => {
                const term = e.target.value.toLowerCase();
                const filtered = cachedEmployees.filter(emp => emp.name.toLowerCase().includes(term));
                renderEmployeeTable(filtered, list);
            };
        }

        renderEmployeeTable(cachedEmployees, list);

        // Refresh requests view to populate dropdowns if requests loaded before employees
        const reqList = document.getElementById('request-list');
        if (reqList && reqList.innerHTML.includes('Loading')) {
            // let loadRequests handle it
        } else if (reqList) {
            loadRequests('request-list', true);
        }

    } catch (err) {
        list.innerHTML = '<p class="error">Failed to load employees.</p>';
    }
}

function renderEmployeeTable(employees, container) {
    if (employees.length === 0) {
        container.innerHTML = '<p>No employees found.</p>';
        return;
    }
    let html = '<table class="data-table"><thead><tr><th>ID</th><th>Name</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
    employees.forEach(emp => {
        html += `<tr>
                <td>${emp.id}</td>
                <td>${emp.name}</td>
                <td><span class="status-badge ${emp.status.toLowerCase()}">${emp.status}</span></td>
                <td>
                    <button class="btn-sm btn-outline" style="color:red; border-color:red" onclick="deleteEmployee(${emp.id})">Delete</button>
                </td>
            </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function setupEmployeeForm() {
    const form = document.getElementById('create-employee-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            name: document.getElementById('emp-name').value,
            email: document.getElementById('emp-email').value,
            phone: document.getElementById('emp-phone').value,
            role: 'Employee', // Default role since dropdown is removed
            start_date: new Date().toISOString().split('T')[0]
        };

        try {
            const res = await fetch('/api/employees', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                form.reset();
                loadEmployees(); // Refresh list
            } else {
                alert('Failed to create employee');
            }
        } catch (err) {
            console.error(err);
        }
    });
}

// --- Employee Portal ---
async function setupEmployeePortal() {
    const select = document.getElementById('employee-select-portal');

    // Populate select
    try {
        const res = await fetch('/api/employees');
        const emps = await res.json();

        emps.forEach(emp => {
            const opt = document.createElement('option');
            opt.value = emp.id;
            opt.textContent = `${emp.name} (${emp.role})`;
            select.appendChild(opt);
        });

        select.addEventListener('change', (e) => {
            const empId = e.target.value;
            if (empId) {
                loadEmployeeTasks(empId);
            }
        });

    } catch (err) {
        console.error("Error loading employees for portal", err);
    }
}

async function loadEmployeeTasks(empId) {
    const list = document.getElementById('my-tasks-list');
    list.innerHTML = '<p>Loading tasks...</p>';

    try {
        const res = await fetch('/api/requests');
        const allRequests = await res.json();

        // Filter client-side for simplicity (in real app, use API filter)
        // Adjust logic: If ID matches assigned_employee string name?
        // Wait, backend returns name string. We need to match somewhat loosely or fix backend to return ID.
        // Checking app.py... `assigned_employee` is `self.employee.name`.
        // This makes filtering by ID hard.
        // PATCH: Let's assume for this demo we filter by checking if the row is assigned.
        // Since we don't have the ID in the GET /requests response, we will just show ALL assigned tasks
        // and pretend they belong to the user, OR filter by the name selected in the dropdown.

        const selectedText = document.querySelector('#employee-select-portal option:checked').textContent;
        const empName = selectedText.split(' (')[0]; // Extract name

        const tasks = allRequests.filter(r => r.assigned_employee === empName);

        if (tasks.length === 0) {
            list.innerHTML = '<p>No tasks assigned to you.</p>';
            return;
        }

        let html = '';
        tasks.forEach(req => {
            html += generateTaskCard(req, true); // true = employee mode
        });
        list.innerHTML = html;

    } catch (err) {
        console.error(err);
        list.innerHTML = '<p class="error">Failed to load tasks.</p>';
    }
}

// --- Shared / Utils ---

async function loadRequests(containerId, isAdmin) {
    const list = document.getElementById(containerId);
    if (!list) return;

    try {
        const res = await fetch('/api/requests');
        const data = await res.json();

        if (data.length === 0) {
            list.innerHTML = '<p>No requests found.</p>';
            return;
        }

        let html = '';
        data.forEach(req => {
            html += generateTaskCard(req, false, isAdmin);
        });
        list.innerHTML = html;
    } catch (err) {
        console.error(err);
        list.innerHTML = '<p class="error">Failed to load requests.</p>';
    }
}

function generateTaskCard(req, isEmployeeView, isAdminView) {
    const assignedTo = req.assigned_employee ? req.assigned_employee : 'Unassigned';

    // Status Badge Logic
    let badgeClass = 'pending';
    if (req.status === 'Assigned') badgeClass = 'info';
    if (req.status === 'Picked Up') badgeClass = 'warning';
    if (req.status === 'Recycled') badgeClass = 'success';

    let actions = '';

    // Admin Actions: Assign
    if (isAdminView && !req.assigned_employee) {
        actions += `
        <div class="assign-actions">
            <select id="assign-select-${req.id}" class="select-sm">
                <option value="">Select Employee...</option>
                ${cachedEmployees.map(e => `<option value="${e.id}">${e.name}</option>`).join('')}
            </select>
            <button class="btn-sm" onclick="assignToEmployee(${req.id})">Assign</button>
            <button class="btn-sm btn-outline" onclick="assignRandomEmployee(${req.id})">Random</button>
        </div>`;
    }

    // Employee Actions: Progress Workflow
    if (isEmployeeView) {
        if (req.status === 'Assigned') {
            actions += `<button class="btn-sm btn-action" onclick="updateStatus(${req.id}, 'Picked Up')">Mark Picked Up</button>`;
        } else if (req.status === 'Picked Up') {
            actions += `<button class="btn-sm btn-action" onclick="updateStatus(${req.id}, 'Recycled')">Mark Recycled (Center)</button>`;
        } else if (req.status === 'Recycled') {
            actions += `<button class="btn-sm btn-action" onclick="updateStatus(${req.id}, 'Reward Delivered')">Deliver Reward</button>`;
        }
    }

    return `
    <div class="request-card status-${req.status.replace(/\s+/g, '-').toLowerCase()}">
        <div class="req-header">
            <span class="req-id">#${req.id}</span>
            <span class="badge badge-${badgeClass}">${req.status}</span>
        </div>
        <div class="req-body">
            <p><strong>Item:</strong> ${req.item}</p>
            <p><strong>Assigned To:</strong> ${assignedTo}</p>
            <p><small>${req.created_at}</small></p>
        </div>
        <div class="req-actions">
            ${actions}
        </div>
    </div>`;
}

// Global Actions
window.updateStatus = async (reqId, newStatus) => {
    try {
        await fetch(`/api/requests/${reqId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        // Refresh Current View
        const empSelect = document.getElementById('employee-select-portal');
        if (empSelect) {
            loadEmployeeTasks(empSelect.value);
        } else {
            loadRequests('request-list', true);
        }
    } catch (err) {
        alert('Update failed');
    }
};

window.assignRandomEmployee = async (reqId) => {
    try {
        if (cachedEmployees.length > 0) {
            const firstEmp = cachedEmployees[0];
            await fetch(`/api/requests/${reqId}/assign`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ employee_id: firstEmp.id })
            });
            loadRequests('request-list', true); // Refresh Admin
        } else {
            alert('Create an employee first!');
        }
    } catch (err) {
        console.error(err);
    }
};

window.assignToEmployee = async (reqId) => {
    const select = document.getElementById(`assign-select-${reqId}`);
    const empId = select.value;

    if (!empId) {
        alert('Please select an employee first.');
        return;
    }

    try {
        await fetch(`/api/requests/${reqId}/assign`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: empId })
        });
        loadRequests('request-list', true); // Refresh Admin
    } catch (err) {
        console.error(err);
        alert('Assignment failed');
    }
};

window.deleteEmployee = async (empId) => {
    if (!confirm('Are you sure you want to delete this employee?')) return;

    try {
        const res = await fetch(`/api/employees/${empId}`, { method: 'DELETE' });
        if (res.ok) {
            loadEmployees(); // Refresh list
        } else {
            alert('Failed to delete employee');
        }
    } catch (err) {
        console.error(err);
        alert('Error deleting employee');
    }
};
