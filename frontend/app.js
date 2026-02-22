const API_BASE = 'http://localhost:8000';
const PROGRESS_BASE = 'http://localhost:8001';

// ── DOM refs ──────────────────────────────────────────────
const taskForm   = document.getElementById('task-form');
const titleInput = document.getElementById('title');
const descInput  = document.getElementById('description');
const taskList   = document.getElementById('task-list');
const errorMsg   = document.getElementById('error-message');
const modal      = document.getElementById('progress-modal');
const modalBody  = document.getElementById('modal-body');
const modalClose = document.getElementById('modal-close');

// ── Helpers ───────────────────────────────────────────────
function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove('hidden');
  setTimeout(() => errorMsg.classList.add('hidden'), 5000);
}

function formatDate(iso) {
  return new Date(iso).toLocaleString();
}

function statusLabel(status) {
  return status.replace('_', ' ');
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// ── Render ────────────────────────────────────────────────
function renderTask(task) {
  const li = document.createElement('li');
  li.className = 'task-card';
  li.dataset.id = task.id;

  const isPending    = task.status === 'pending';
  const isInProgress = task.status === 'in_progress';

  li.innerHTML = `
    <div class="task-info">
      <div class="task-title">${escHtml(task.title)}</div>
      ${task.description ? `<div class="task-description">${escHtml(task.description)}</div>` : ''}
      <span class="status-badge status-${task.status}">${statusLabel(task.status)}</span>
      <div class="task-meta">Created ${formatDate(task.created_at)}</div>
    </div>
    <div class="task-actions">
      ${isPending    ? `<button class="btn-start"    data-action="start"    data-id="${task.id}">Start</button>` : ''}
      ${isInProgress ? `<button class="btn-complete" data-action="complete" data-id="${task.id}">Complete</button>` : ''}
      <button class="btn-history" data-action="history" data-id="${task.id}">History</button>
      <button class="btn-delete"  data-action="delete"  data-id="${task.id}">Delete</button>
    </div>
  `;
  return li;
}

async function loadTasks() {
  try {
    const res = await fetch(`${API_BASE}/tasks`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const tasks = await res.json();
    taskList.innerHTML = '';
    if (tasks.length === 0) {
      taskList.innerHTML = '<li style="color:#6b7280;font-size:0.875rem;">No tasks yet. Add one above!</li>';
      return;
    }
    tasks.forEach(t => taskList.appendChild(renderTask(t)));
  } catch (err) {
    showError(`Failed to load tasks: ${err.message}`);
  }
}

// ── Task actions ──────────────────────────────────────────
async function createTask(title, description) {
  try {
    const res = await fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    await loadTasks();
  } catch (err) {
    showError(`Failed to create task: ${err.message}`);
  }
}

async function updateStatus(id, status) {
  try {
    const res = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    await loadTasks();
  } catch (err) {
    showError(`Failed to update task: ${err.message}`);
  }
}

async function deleteTask(id) {
  try {
    const res = await fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    await loadTasks();
  } catch (err) {
    showError(`Failed to delete task: ${err.message}`);
  }
}

async function showHistory(id) {
  modalBody.innerHTML = '<p class="no-events">Loading…</p>';
  modal.classList.remove('hidden');
  try {
    const res = await fetch(`${PROGRESS_BASE}/progress/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const events = await res.json();
    if (events.length === 0) {
      modalBody.innerHTML = '<p class="no-events">No events recorded.</p>';
      return;
    }
    modalBody.innerHTML = events.map(e => `
      <div class="event-item">
        <div class="event-type">${e.event_type}</div>
        <div class="event-details">
          ${e.old_status ? `<span>${statusLabel(e.old_status)}</span> → ` : ''}
          ${e.new_status ? `<span>${statusLabel(e.new_status)}</span>` : '—'}
        </div>
        <div class="event-time">${formatDate(e.timestamp)}</div>
      </div>
    `).join('');
  } catch (err) {
    modalBody.innerHTML = `<p class="no-events" style="color:#991b1b;">Error: ${err.message}</p>`;
  }
}

// ── Event listeners ───────────────────────────────────────
taskForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = titleInput.value.trim();
  const desc  = descInput.value.trim();
  if (!title) return;
  await createTask(title, desc);
  taskForm.reset();
});

// Event delegation on task list
taskList.addEventListener('click', async (e) => {
  const btn = e.target.closest('button[data-action]');
  if (!btn) return;
  const { action, id } = btn.dataset;
  if (action === 'start')    await updateStatus(id, 'in_progress');
  if (action === 'complete') await updateStatus(id, 'completed');
  if (action === 'delete')   await deleteTask(id);
  if (action === 'history')  await showHistory(id);
});

modalClose.addEventListener('click', () => modal.classList.add('hidden'));
modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.add('hidden'); });

// ── Init ──────────────────────────────────────────────────
loadTasks();
