// dashboard.js — ScamPay Dashboard Logic

document.addEventListener('DOMContentLoaded', () => {
  renderDashboard();

  document.getElementById('clearHistory')?.addEventListener('click', () => {
    if (confirm('Clear all scan history?')) {
      window.ScamPayHistory.clearHistory();
      renderDashboard();
    }
  });

  document.getElementById('historySearch')?.addEventListener('input', (e) => {
    filterHistory(e.target.value.toLowerCase());
  });
});

function renderDashboard() {
  const history = window.ScamPayHistory.getHistory();
  updateSummaryCards(history);
  updateRiskBreakdown(history);
  updateScamTypes(history);
  renderHistoryList(history);
}

function updateSummaryCards(history) {
  const total = history.length;
  const scams = history.filter(h => h.score >= 61).length;
  const safe = history.filter(h => h.score < 31).length;
  const avgScamAmount = 4800; // illustrative estimate per scam
  const saved = scams * avgScamAmount;

  document.getElementById('totalScans').textContent = total;
  document.getElementById('scamsFound').textContent = scams;
  document.getElementById('safeMsgs').textContent = safe;
  document.getElementById('moneySaved').textContent = saved >= 1000
    ? `₹${(saved / 1000).toFixed(1)}K`
    : `₹${saved}`;
}

function updateRiskBreakdown(history) {
  const total = Math.max(history.length, 1);
  const counts = { vh: 0, h: 0, m: 0, l: 0 };
  history.forEach(h => {
    if (h.score >= 81) counts.vh++;
    else if (h.score >= 61) counts.h++;
    else if (h.score >= 31) counts.m++;
    else counts.l++;
  });
  document.getElementById('barVH').style.width = (counts.vh / total * 100) + '%';
  document.getElementById('barH').style.width  = (counts.h  / total * 100) + '%';
  document.getElementById('barM').style.width  = (counts.m  / total * 100) + '%';
  document.getElementById('barL').style.width  = (counts.l  / total * 100) + '%';
  document.getElementById('countVH').textContent = counts.vh;
  document.getElementById('countH').textContent  = counts.h;
  document.getElementById('countM').textContent  = counts.m;
  document.getElementById('countL').textContent  = counts.l;
}

function updateScamTypes(history) {
  const el = document.getElementById('scamTypesList');
  if (!history.length) {
    el.innerHTML = '<div class="empty-state">No scans yet. <a href="scan.html">Start scanning →</a></div>';
    return;
  }
  const counts = {};
  history.forEach(h => {
    if (h.category && h.category !== 'No Scam Detected') {
      const key = h.category.split(' + ')[0];
      counts[key] = (counts[key] || 0) + 1;
    }
  });
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
  if (!sorted.length) {
    el.innerHTML = '<p style="color:var(--muted);font-size:14px">No scam types detected yet.</p>';
    return;
  }
  el.innerHTML = sorted.map(([name, count]) => `
    <div class="scam-type-item">
      <span class="scam-type-name">${name}</span>
      <span class="scam-type-count">${count}</span>
    </div>
  `).join('');
}

function renderHistoryList(history, filter = '') {
  const el = document.getElementById('historyList');
  const emptyEl = document.getElementById('emptyHistory');

  const filtered = filter
    ? history.filter(h => h.text?.toLowerCase().includes(filter) || h.category?.toLowerCase().includes(filter))
    : history;

  if (!filtered.length) {
    el.innerHTML = '';
    if (emptyEl) {
      emptyEl.style.display = 'block';
      el.appendChild(emptyEl);
    }
    return;
  }

  if (emptyEl) emptyEl.style.display = 'none';

  const ringClass = (lvl) => ({ 'very-high': 'ring-red', high: 'ring-orange', medium: 'ring-yellow', low: 'ring-green' }[lvl] || 'ring-green');
  const badgeClass = (lvl) => ({ 'very-high': 'risk-red', high: 'risk-orange', medium: 'risk-yellow', low: 'risk-green' }[lvl] || 'risk-green');
  const badgeLabel = (lvl) => ({ 'very-high': '🔴 Very High', high: '🟠 High', medium: '🟡 Medium', low: '🟢 Low' }[lvl] || '🟢 Low');

  el.innerHTML = filtered.map(item => {
    const date = new Date(item.timestamp).toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
    return `
      <div class="history-item">
        <div class="history-score ${ringClass(item.riskLevel)}">${item.score}</div>
        <div class="history-content">
          <div class="history-text">${escapeHtml(item.text || '(No preview)')}</div>
          <div class="history-meta">${item.category || 'N/A'} · ${date}</div>
        </div>
        <span class="history-badge ${badgeClass(item.riskLevel)}">${badgeLabel(item.riskLevel)}</span>
      </div>
    `;
  }).join('');
}

function filterHistory(query) {
  const history = window.ScamPayHistory.getHistory();
  renderHistoryList(history, query);
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
