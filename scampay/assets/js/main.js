// main.js — Shared utilities for ScamPay

// ============================================
// DARK / LIGHT MODE
// ============================================
const THEME_KEY = 'scampay_theme';

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);
  // Update every toggle button on the page
  document.querySelectorAll('.theme-toggle').forEach(btn => {
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
    btn.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
  });
}

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  // Default to system preference if no saved choice
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? 'dark' : 'light'));
}

// Run immediately so there's no flash of wrong theme
initTheme();

document.addEventListener('DOMContentLoaded', () => {
  // Theme toggle button
  document.getElementById('themeToggle')?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });

  // NAV TOGGLE (mobile)
  document.getElementById('navToggle')?.addEventListener('click', () => {
    document.querySelector('.nav-links')?.classList.toggle('open');
  });

  // Close nav on link click (mobile)
  document.querySelectorAll('.nav-links a').forEach(a => {
    a.addEventListener('click', () => {
      document.querySelector('.nav-links')?.classList.remove('open');
    });
  });
});

// ============================================
// HISTORY UTILITIES (localStorage)
// ============================================
const HISTORY_KEY = 'scampay_history';

function getHistory() {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); }
  catch { return []; }
}

function saveToHistory(entry) {
  const history = getHistory();
  history.unshift({ ...entry, id: Date.now(), timestamp: new Date().toISOString() });
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 100)));
}

function clearHistory() {
  localStorage.removeItem(HISTORY_KEY);
}

window.ScamPayHistory = { getHistory, saveToHistory, clearHistory };
