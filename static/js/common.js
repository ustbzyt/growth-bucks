// common.js: Common utility functions
function fetchBehaviors() {
    return fetch('/behaviors').then(r => {
        if (!r.ok) throw new Error('Failed to fetch behavior list');
        return r.json();
    });
}
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, function (c) {
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c];
    });
}
