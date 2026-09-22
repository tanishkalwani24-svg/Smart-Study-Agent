// report.js — Report page logic

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reportForm');
  const successEl = document.getElementById('reportSuccess');

  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    // In a real app, this would POST to an API
    // Here we save to localStorage community reports
    const report = {
      id: Date.now(),
      scamType: formData.get('scamType'),
      platform: formData.get('platform'),
      identifier: formData.get('identifier'),
      description: formData.get('description'),
      amount: formData.get('amount'),
      timestamp: new Date().toISOString(),
    };
    const reports = JSON.parse(localStorage.getItem('scampay_reports') || '[]');
    reports.unshift(report);
    localStorage.setItem('scampay_reports', JSON.stringify(reports.slice(0, 200)));

    form.style.display = 'none';
    successEl.style.display = 'block';
    successEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
