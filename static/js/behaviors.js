// behaviors.js: Behavior table rendering logic
function renderBehaviorsByCategory(behaviors, container) {
    if (!Array.isArray(behaviors) || behaviors.length === 0) {
        container.innerHTML = '<div class="alert alert-warning">No behavior data available</div>';
        return;
    }
    // Group by category
    const groups = {};
    behaviors.forEach(b => {
        if (!groups[b.category]) groups[b.category] = [];
        groups[b.category].push(b);
    });
    container.innerHTML = '';
    Object.keys(groups).sort().forEach(cat => {
        const title = document.createElement('div');
        title.className = 'category-title';
        title.textContent = cat;
        const table = document.createElement('table');
        table.className = 'table table-bordered table-striped table-category';
        table.innerHTML = `<thead><tr><th>Name</th><th>Points</th><th>Description</th><th>Frequency</th></tr></thead>`;
        const tbody = document.createElement('tbody');
        groups[cat].forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${escapeHtml(b.name)}</td><td>${b.points}</td><td>${escapeHtml(b.desc)}</td><td>${escapeHtml(b.frequency)}</td>`;
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        container.appendChild(title);
        container.appendChild(table);
    });
}

function renderBehaviorsByFrequency(behaviors, container) {
    if (!Array.isArray(behaviors) || behaviors.length === 0) {
        container.innerHTML = '<div class="alert alert-warning">No behavior data available</div>';
        return;
    }
    // Group by frequency
    const groups = {};
    behaviors.forEach(b => {
        if (!groups[b.frequency]) groups[b.frequency] = [];
        groups[b.frequency].push(b);
    });
    container.innerHTML = '';
    Object.keys(groups).sort().forEach(freq => {
        const title = document.createElement('div');
        title.className = 'frequency-title';
        title.textContent = freq;
        const table = document.createElement('table');
        table.className = 'table table-bordered table-striped table-category';
        table.innerHTML = `<thead><tr><th>Name</th><th>Points</th><th>Description</th><th>Category</th></tr></thead>`;
        const tbody = document.createElement('tbody');
        groups[freq].forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${escapeHtml(b.name)}</td><td>${b.points}</td><td>${escapeHtml(b.desc)}</td><td>${escapeHtml(b.category)}</td>`;
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        container.appendChild(title);
        container.appendChild(table);
    });
}
