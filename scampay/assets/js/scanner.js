// scanner.js — ScamPay scam detection engine

// ============================================
// DETECTION DATA
// ============================================
const SCAM_KEYWORDS = {
  otp:        ['otp', 'one time password', 'verification code', 'verify code', 'share otp', 'enter otp', 'otp ko share'],
  kyc:        ['kyc', 'know your customer', 'kyc expired', 'kyc update', 'kyc verification', 'complete kyc', 'kyc pending'],
  upi:        ['upi', 'collect request', 'upi pin', 'upi id', 'bhim', 'payment link', 'qr code', 'pay now', 'send money'],
  urgency:    ['urgent', 'immediately', 'expire', 'blocked', 'suspend', 'last chance', 'within 24', '24 hours', 'right now', 'act fast', 'limited time', 'today only'],
  reward:     ['won', 'winner', 'lottery', 'lucky draw', 'prize', 'reward', 'congratulations', 'selected', 'gift', 'cashback', 'bonus'],
  investment: ['guaranteed return', 'double money', 'profit', '% return', 'invest now', 'scheme', 'trading group', 'stock tips', 'forex'],
  support:    ['customer care', 'helpline', 'support team', 'bank official', 'rbi officer', 'government officer', 'technical team'],
  refund:     ['refund', 'reimbursement', 'get money back', 'payment failed', 'scan to receive', 'receive money'],
  phishing:   ['click here', 'login', 'verify account', 'confirm details', 'update now', 'access link', 'open link'],
  pin:        ['pin', 'mpin', 'net banking password', 'card number', 'cvv', 'expiry'],
};

const SUSPICIOUS_DOMAINS = ['bit.ly', 'tinyurl', 'goo.gl', 'shorturl', 't.co', 'ow.ly', 'is.gd',
  '.tk', '.cf', '.ga', '.ml', '.gq', 'ngrok', 'heroku', 'glitch', 'free', '-bank-', '-hdfc-', '-sbi-', '-paytm-', '-phonepe-'];

const SUSPICIOUS_UPI_PATTERNS = [
  /kyc/i, /verify/i, /update/i, /secure/i, /helpline/i, /support/i, /refund/i,
  /prize/i, /reward/i, /lottery/i, /win/i, /lucky/i, /bank-?official/i,
  /99+\d*@/i,
];

const SCAM_TYPES_LABELS = {
  otp: '🔑 OTP Scam',
  kyc: '📋 KYC Scam',
  upi: '💳 UPI Fraud',
  support: '📞 Fake Customer Care',
  reward: '🏆 Lottery/Reward Scam',
  investment: '📈 Investment Fraud',
  phishing: '🎣 Phishing Link',
  refund: '💸 Refund Scam',
  urgency: '⚠️ Urgency Manipulation',
  pin: '🔒 PIN/Password Theft',
};

// ============================================
// EXTRACTION FUNCTIONS
// ============================================
function extractUPI(text) {
  const matches = text.match(/[\w.\-+]+@[\w]+/gi) || [];
  return matches.filter(m => m.includes('@'));
}

function extractPhones(text) {
  return (text.match(/(?:91)?[6-9]\d{9}/g) || []).map(p => p.replace(/^91/, ''));
}

function extractURLs(text) {
  return text.match(/https?:\/\/[^\s]+|www\.[^\s]+|[a-z0-9\-]+\.(tk|cf|ga|ml|gq|xyz|info|loan|online|site|shop)/gi) || [];
}

function extractEmails(text) {
  return text.match(/[\w.+-]+@[\w-]+\.[a-z]{2,}/gi) || [];
}

function extractAmount(text) {
  const matches = text.match(/₹\s*[\d,]+|rs\.?\s*[\d,]+|\d+\s*rupees?/gi) || [];
  return matches;
}

// ============================================
// ANALYSIS ENGINE
// ============================================
function analyzeText(rawText) {
  const text = rawText.toLowerCase();
  const findings = [];
  const triggeredTypes = {};
  let score = 0;

  // Check each keyword category
  for (const [cat, words] of Object.entries(SCAM_KEYWORDS)) {
    const hits = words.filter(w => text.includes(w));
    if (hits.length > 0) {
      triggeredTypes[cat] = hits;
      const weight = {
        otp: 35, kyc: 25, pin: 30, upi: 20,
        urgency: 15, reward: 20, refund: 20,
        support: 15, investment: 20, phishing: 25,
      }[cat] || 10;
      score += Math.min(weight, weight * (1 + (hits.length - 1) * 0.3));
    }
  }

  // Extraction
  const upis = extractUPI(rawText);
  const phones = extractPhones(rawText);
  const urls = extractURLs(rawText);
  const emails = extractEmails(rawText);
  const amounts = extractAmount(rawText);

  // UPI suspicion check
  upis.forEach(upi => {
    if (SUSPICIOUS_UPI_PATTERNS.some(p => p.test(upi))) {
      score += 25;
      findings.push({ icon: '💳', text: `Suspicious UPI ID detected: ${upi}` });
    }
  });

  // URL suspicion
  urls.forEach(url => {
    const suspicious = SUSPICIOUS_DOMAINS.some(d => url.toLowerCase().includes(d));
    if (suspicious) {
      score += 30;
      findings.push({ icon: '🔗', text: `Suspicious URL found: ${url}` });
    } else {
      score += 10;
      findings.push({ icon: '🔗', text: `External URL detected: ${url}` });
    }
  });

  // Build human-readable findings from triggered types
  if (triggeredTypes.otp) findings.push({ icon: '🔑', text: 'OTP requested — never share OTPs with anyone' });
  if (triggeredTypes.pin) findings.push({ icon: '🔒', text: 'PIN/Password requested — legitimate services never ask for this' });
  if (triggeredTypes.kyc) findings.push({ icon: '📋', text: 'KYC update demanded — verify directly via official app' });
  if (triggeredTypes.upi) findings.push({ icon: '💳', text: 'UPI payment or collect request detected' });
  if (triggeredTypes.urgency) findings.push({ icon: '⏰', text: 'Urgency language used to pressure you into acting fast' });
  if (triggeredTypes.reward) findings.push({ icon: '🏆', text: 'Lottery/reward claim — classic scam tactic' });
  if (triggeredTypes.refund) findings.push({ icon: '💸', text: 'Refund scam pattern — you scan QR to "receive" but pay instead' });
  if (triggeredTypes.support) findings.push({ icon: '📞', text: 'Fake customer care impersonation detected' });
  if (triggeredTypes.investment) findings.push({ icon: '📈', text: 'Fraudulent investment scheme language detected' });
  if (triggeredTypes.phishing) findings.push({ icon: '🎣', text: 'Phishing attempt — asking you to click a link and enter credentials' });

  // Payment amounts with urgent language = extra risk
  if (amounts.length > 0 && triggeredTypes.urgency) {
    score += 10;
    findings.push({ icon: '₹', text: `Payment demand detected: ${amounts.join(', ')}` });
  }

  score = Math.min(Math.round(score), 100);

  // Determine scam category label
  const topTypes = Object.keys(triggeredTypes);
  const categoryLabels = topTypes.slice(0, 2).map(t => SCAM_TYPES_LABELS[t]?.replace(/^[^\s]+\s/, '') || t);
  const category = categoryLabels.length ? categoryLabels.join(' + ') : 'No Scam Detected';

  return {
    score,
    category,
    triggeredTypes: topTypes,
    findings,
    extracted: { upis, phones, urls, emails, amounts },
    riskLevel: getRiskLevel(score),
  };
}

function getRiskLevel(score) {
  if (score >= 81) return { level: 'very-high', label: '🔴 Very High Risk', color: '#dc2626' };
  if (score >= 61) return { level: 'high',      label: '🟠 High Risk',      color: '#ea580c' };
  if (score >= 31) return { level: 'medium',    label: '🟡 Medium Risk',    color: '#d97706' };
  return                  { level: 'low',       label: '🟢 Low Risk',       color: '#16a34a' };
}

function getAdvice(result) {
  const advice = [];
  const { triggeredTypes, extracted } = result;
  if (triggeredTypes.includes('otp'))   advice.push({ icon: '🚫', text: 'Never share your OTP with anyone — not even bank officials.' });
  if (triggeredTypes.includes('pin'))   advice.push({ icon: '🔒', text: 'Never enter your UPI PIN or banking password on unknown links.' });
  if (triggeredTypes.includes('kyc'))   advice.push({ icon: '📱', text: 'Verify KYC only through the official app or your bank branch.' });
  if (extracted.urls.length)            advice.push({ icon: '🔗', text: "Don't click suspicious links. Type the official website address directly." });
  if (triggeredTypes.includes('upi'))   advice.push({ icon: '💳', text: 'Decline or ignore unknown UPI collect requests immediately.' });
  if (triggeredTypes.includes('reward'))advice.push({ icon: '🎁', text: 'Ignore prize/lottery claims — real prizes never require upfront payment.' });
  if (triggeredTypes.includes('refund'))advice.push({ icon: '💸', text: 'To receive a refund, you scan a QR — you NEVER need to enter a PIN.' });
  if (result.score >= 61) {
    advice.push({ icon: '📞', text: 'Report this scam: Call 1930 or visit cybercrime.gov.in' });
    advice.push({ icon: '🚨', text: "Block the sender and don't respond to this message." });
  }
  if (advice.length === 0) advice.push({ icon: '✅', text: 'No immediate red flags, but always stay cautious with unknown senders.' });
  return advice;
}

// ============================================
// WHERE TO REPORT — context-aware per scam type
// ============================================
function getReportingTargets(result) {
  const { triggeredTypes, extracted, score } = result;
  if (score < 31) return [];  // low risk — no urgent reporting needed

  const targets = [];

  // ── 1. ALWAYS: Cyber Crime Portal + 1930 for any medium+ risk ──────────────
  targets.push({
    priority: 'primary',
    icon: '🏛️',
    name: 'National Cyber Crime Portal',
    shortName: 'Cyber Crime',
    why: 'For all types of online financial fraud — file a formal complaint and get a reference number.',
    steps: ['Visit cybercrime.gov.in', 'Click "Report Cyber Crime"', 'Select "Financial Fraud"', 'Fill the form & note complaint number'],
    contact: 'cybercrime.gov.in',
    contactUrl: 'https://cybercrime.gov.in',
    btnLabel: 'File Complaint →',
  });

  targets.push({
    priority: 'primary',
    icon: '📞',
    name: '1930 — Cyber Fraud Helpline',
    shortName: '1930 Helpline',
    why: 'Call immediately if money was lost. The sooner you call, the higher the chance of fund recovery.',
    steps: ['Dial 1930', 'Say "I received a scam message"', 'Provide transaction details if any', 'Note the complaint ID given'],
    contact: '1930',
    contactUrl: 'tel:1930',
    btnLabel: '📞 Call 1930 Now',
    urgent: true,
  });

  // ── 2. KYC SCAM → Bank ──────────────────────────────────────────────────────
  if (triggeredTypes.includes('kyc') || triggeredTypes.includes('support')) {
    targets.push({
      priority: 'secondary',
      icon: '🏦',
      name: 'Your Bank / Wallet Provider',
      shortName: 'Bank Helpline',
      why: 'KYC scams impersonate your bank. Call your bank directly to report the fraud number and protect your account.',
      steps: [
        'Call your bank\'s official helpline (back of your debit card)',
        'Report the fraudulent UPI ID / phone number',
        'Ask them to block any suspicious transactions',
        'Change your net banking password immediately',
      ],
      contact: 'SBI: 1800-11-2211 · HDFC: 1800-258-6161 · ICICI: 1800-1080 · PayTM: 1800-102-8282',
      contactUrl: null,
      btnLabel: null,
      bankNumbers: [
        { name: 'SBI',     number: '18001112211' },
        { name: 'HDFC',    number: '18002586161' },
        { name: 'ICICI',   number: '18001080'    },
        { name: 'Axis',    number: '18604195555' },
        { name: 'PayTM',   number: '18001028282' },
        { name: 'PhonePe', number: '08068727374' },
      ],
    });
  }

  // ── 3. UPI / REFUND SCAM → NPCI / UPI platform ──────────────────────────────
  if (triggeredTypes.includes('upi') || triggeredTypes.includes('refund')) {
    targets.push({
      priority: 'secondary',
      icon: '💳',
      name: 'NPCI / UPI App Support',
      shortName: 'NPCI & UPI',
      why: 'Report the fraudulent UPI ID to NPCI and the payment app. They can block the handle and freeze collected funds.',
      steps: [
        'Open your UPI app (PhonePe / GPay / PayTM / BHIM)',
        'Go to Help → Report a Fraud',
        'Enter the suspicious UPI ID or transaction ID',
        'Also report at npci.org.in/contact',
      ],
      contact: 'npci.org.in',
      contactUrl: 'https://www.npci.org.in/contact',
      btnLabel: 'Report to NPCI →',
    });
  }

  // ── 4. PHISHING LINK → CERT-In + TRAI Chakshu ──────────────────────────────
  if (triggeredTypes.includes('phishing') || extracted.urls.length > 0) {
    targets.push({
      priority: 'secondary',
      icon: '🔗',
      name: 'CERT-In (Phishing Link Report)',
      shortName: 'CERT-In',
      why: 'India\'s cybersecurity agency. Report phishing URLs so they can block the domain for all users.',
      steps: [
        'Visit incident.cert-in.org.in',
        'Select "Phishing" as incident type',
        'Paste the suspicious URL',
        'Submit — CERT-In will investigate & block',
      ],
      contact: 'incident.cert-in.org.in',
      contactUrl: 'https://incident.cert-in.org.in',
      btnLabel: 'Report URL →',
    });
  }

  // ── 5. SMS / CALL scam → TRAI Chakshu ───────────────────────────────────────
  if (triggeredTypes.includes('support') || extracted.phones.length > 0) {
    targets.push({
      priority: 'secondary',
      icon: '📡',
      name: 'Chakshu Portal (TRAI)',
      shortName: 'Chakshu / TRAI',
      why: 'Report the scam SMS or call number so TRAI can disconnect the telecom connection used by fraudsters.',
      steps: [
        'Visit sancharsaathi.gov.in/sfc',
        'Select message / call type',
        'Enter the suspicious number',
        'Submit — TRAI will block the number',
      ],
      contact: 'sancharsaathi.gov.in',
      contactUrl: 'https://sancharsaathi.gov.in/sfc/Home/sfc-complaint.jsp',
      btnLabel: 'Report on Chakshu →',
    });
  }

  // ── 6. LOTTERY / INVESTMENT FRAUD → RBI / SEBI ──────────────────────────────
  if (triggeredTypes.includes('reward') || triggeredTypes.includes('investment')) {
    targets.push({
      priority: 'secondary',
      icon: '📈',
      name: 'SEBI / RBI (Investment / Lottery Fraud)',
      shortName: 'SEBI · RBI',
      why: 'Fake investment schemes and lottery frauds fall under RBI and SEBI jurisdiction. Report here to get them investigated.',
      steps: [
        'Investment fraud → scores.sebi.gov.in',
        'Banking / RBI fraud → bankingombudsman.rbi.org.in',
        'Provide all transaction details and screenshots',
        'You can also email: rbi@rbi.org.in',
      ],
      contact: 'scores.sebi.gov.in · rbi.org.in',
      contactUrl: 'https://scores.sebi.gov.in',
      btnLabel: 'Report to SEBI →',
    });
  }

  return targets;
}

// ──────────────────────────────────────────────
// Renders the "Where to Report" HTML block
// ──────────────────────────────────────────────
function renderReportingSection(result) {
  const targets = getReportingTargets(result);
  if (!targets.length) return '';

  const primaryTargets   = targets.filter(t => t.priority === 'primary');
  const secondaryTargets = targets.filter(t => t.priority === 'secondary');

  function renderCard(t) {
    const bankBtns = t.bankNumbers
      ? t.bankNumbers.map(b =>
          `<a href="tel:${b.number}" class="bank-call-btn">📞 ${b.name}</a>`
        ).join('')
      : '';

    const stepsHTML = t.steps.map((s, i) =>
      `<div class="report-step"><span class="report-step-num">${i + 1}</span><span>${s}</span></div>`
    ).join('');

    const actionBtn = t.contactUrl
      ? `<a href="${t.contactUrl}" target="${t.contactUrl.startsWith('tel') ? '_self' : '_blank'}" class="btn ${t.urgent ? 'btn-danger' : 'btn-primary'} btn-sm">${t.btnLabel}</a>`
      : '';

    return `
      <div class="report-target-card ${t.urgent ? 'report-urgent' : ''}">
        <div class="report-card-header">
          <span class="report-icon">${t.icon}</span>
          <div class="report-card-title">
            <h4>${t.name}</h4>
            <p class="report-card-why">${t.why}</p>
          </div>
        </div>
        <div class="report-steps-list">${stepsHTML}</div>
        ${bankBtns ? `<div class="bank-btns-row">${bankBtns}</div>` : ''}
        <div class="report-card-footer">
          <span class="report-contact-label">${t.contact}</span>
          ${actionBtn}
        </div>
      </div>
    `;
  }

  return `
    <div class="reporting-section">
      <div class="reporting-header">
        <span class="reporting-header-icon">🚨</span>
        <div>
          <h3>Where to Report This Scam</h3>
          <p>Based on the scam type detected, here are the exact authorities to contact — in order of priority</p>
        </div>
      </div>

      <div class="report-priority-label">⚡ Act First — Do These Immediately</div>
      <div class="report-targets-grid primary-grid">
        ${primaryTargets.map(renderCard).join('')}
      </div>

      ${secondaryTargets.length ? `
        <div class="report-priority-label secondary-lbl">📋 Also Report Here (Based on Your Scam Type)</div>
        <div class="report-targets-grid secondary-grid">
          ${secondaryTargets.map(renderCard).join('')}
        </div>
      ` : ''}
    </div>
  `;
}

// ============================================
// IDENTIFIER ANALYSIS (UPI / Phone / URL / Email)
// ============================================
function analyzeIdentifier(type, value) {
  let score = 0;
  const findings = [];
  const val = value.toLowerCase().trim();

  if (type === 'upi') {
    if (SUSPICIOUS_UPI_PATTERNS.some(p => p.test(val))) {
      score += 55;
      findings.push({ icon: '💳', text: `UPI handle "${value}" contains suspicious keywords` });
    }
    if (!val.includes('@')) {
      score += 10;
      findings.push({ icon: '⚠️', text: 'Not a valid UPI ID format' });
    }
    const known_safe = ['@paytm', '@oksbi', '@okaxis', '@okhdfcbank', '@ybl', '@ibl', '@axl', '@pthdfc'];
    if (!known_safe.some(d => val.endsWith(d))) {
      score += 10;
      findings.push({ icon: 'ℹ️', text: 'UPI handle is not from a commonly recognised bank' });
    }
  }

  if (type === 'url') {
    const suspicious = SUSPICIOUS_DOMAINS.some(d => val.includes(d));
    if (suspicious) {
      score += 60;
      findings.push({ icon: '🔗', text: `URL contains suspicious domain patterns` });
    }
    if (!val.startsWith('https')) {
      score += 20;
      findings.push({ icon: '🔓', text: 'URL is not HTTPS — potentially unsafe' });
    }
    if (/bank|hdfc|sbi|icici|paytm|phonepe|npci|rbi|upi|kyc|verify|secure|login|update/i.test(val) && !val.includes('.gov')) {
      score += 35;
      findings.push({ icon: '🎣', text: 'URL mimics a banking/financial institution — likely phishing' });
    }
  }

  if (type === 'phone') {
    if (!/^[6-9]\d{9}$/.test(val.replace(/\s/g, ''))) {
      findings.push({ icon: 'ℹ️', text: 'Not a standard Indian mobile number format' });
    } else {
      score += 15;
      findings.push({ icon: '📞', text: 'Phone number noted. Verify against official sources.' });
    }
  }

  if (type === 'email') {
    const suspicious_email_domains = ['gmail', 'yahoo', 'hotmail', 'outlook'];
    const domain = val.split('@')[1] || '';
    if (suspicious_email_domains.some(d => domain.includes(d))) {
      score += 20;
      findings.push({ icon: '📧', text: 'Financial institutions don\'t use personal email domains for official communication' });
    }
    if (/bank|hdfc|sbi|icici|paytm|rbi|npci|support|helpdesk/i.test(val)) {
      score += 35;
      findings.push({ icon: '🎣', text: 'Email impersonates a financial institution — likely phishing' });
    }
  }

  score = Math.min(score, 100);
  return {
    score,
    category: score > 60 ? 'Suspicious Identifier' : score > 30 ? 'Potentially Suspicious' : 'Low Risk',
    triggeredTypes: [],
    findings,
    extracted: { upis: type === 'upi' ? [value] : [], phones: type === 'phone' ? [value] : [], urls: type === 'url' ? [value] : [], emails: type === 'email' ? [value] : [], amounts: [] },
    riskLevel: getRiskLevel(score),
  };
}

// ============================================
// RESULT RENDERER
// ============================================
function renderResult(result, inputPreview) {
  const { score, category, riskLevel, findings, extracted } = result;
  const advice = getAdvice(result);

  const ringClass = { 'very-high': 'ring-red', 'high': 'ring-orange', 'medium': 'ring-yellow', 'low': 'ring-green' }[riskLevel.level];
  const cardClass = `risk-${riskLevel.level}`;

  const findingsHTML = findings.length
    ? findings.map(f => `<div class="finding-item"><span class="finding-icon">${f.icon}</span><span>${f.text}</span></div>`).join('')
    : '<div class="finding-item"><span class="finding-icon">✅</span><span>No obvious scam indicators found in this message.</span></div>';

  const adviceHTML = advice.map(a => `<div class="advice-item"><span class="advice-icon">${a.icon}</span><span>${a.text}</span></div>`).join('');

  const extractedItems = [
    ...extracted.upis.map(u => `<span class="extracted-tag">💳 ${u}</span>`),
    ...extracted.phones.map(p => `<span class="extracted-tag">📞 ${p}</span>`),
    ...extracted.urls.map(u => `<span class="extracted-tag">🔗 ${u.substring(0, 40)}${u.length > 40 ? '…' : ''}</span>`),
    ...extracted.emails.map(e => `<span class="extracted-tag">📧 ${e}</span>`),
    ...extracted.amounts.map(a => `<span class="extracted-tag">₹ ${a}</span>`),
  ];

  const extractedHTML = extractedItems.length
    ? `<div class="extracted-info"><h3>Extracted Entities</h3><div class="extracted-tags">${extractedItems.join('')}</div></div>`
    : '';

  return `
    <div class="result-card ${cardClass}">
      <div class="result-header">
        <div class="big-score-ring ${ringClass}">
          <span>${score}</span>
          <span class="score-denom">/100</span>
        </div>
        <div class="result-meta">
          <h2>${riskLevel.label}</h2>
          <div class="risk-label" style="color:${riskLevel.color}">Risk Score: ${score}/100</div>
          <div class="risk-cat">Category: ${category}</div>
        </div>
      </div>
      <div class="result-findings">
        <h3>🔎 Why This Was Flagged</h3>
        <div class="findings-list">${findingsHTML}</div>
      </div>
      ${extractedHTML}
    </div>

    <div class="safety-section">
      <h3>🛡️ Safety Advice</h3>
      <div class="advice-list">${adviceHTML}</div>
      <div class="result-actions">
        <button class="btn btn-outline" onclick="window.location.reload()">🔍 Scan Another</button>
        <a href="dashboard.html" class="btn btn-outline">📊 View Dashboard</a>
      </div>
    </div>

    ${renderReportingSection(result)}
  `;
}

// ============================================
// MAIN SCAN LOGIC
// ============================================
function runScan() {
  const activeTab = document.querySelector('.tab-panel.active')?.id;
  let inputText = '';
  let displayText = '';
  let scanType = 'text';

  if (activeTab === 'tab-text') {
    inputText = document.getElementById('msgInput')?.value?.trim() || '';
    displayText = inputText;
    scanType = 'message';
    if (!inputText) { alert('Please paste a message to scan.'); return; }
  } else if (activeTab === 'tab-screenshot') {
    // OCR simulation — use extracted text if present, else mock
    inputText = document.getElementById('ocrText')?.value || '';
    if (!inputText) {
      // Simulate OCR extraction with placeholder text
      inputText = 'Dear customer your kyc has expired please click the link to update http://hdfc-kyc-update.tk share your otp to verify';
    }
    displayText = '[Screenshot] ' + inputText.substring(0, 60) + '…';
    scanType = 'screenshot';
  } else if (activeTab === 'tab-identifier') {
    const type  = document.getElementById('idType')?.value || 'upi';
    const value = document.getElementById('idValue')?.value?.trim() || '';
    if (!value) { alert('Please enter an identifier to check.'); return; }
    inputText = value;
    displayText = `${type.toUpperCase()}: ${value}`;
    scanType = type;

    // Show loading
    const btn = document.getElementById('scanBtn');
    const btnText = document.getElementById('scanBtnText');
    const spinner = document.getElementById('scanSpinner');
    btn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';

    setTimeout(() => {
      const result = analyzeIdentifier(type, value);
      const panel = document.getElementById('resultPanel');
      panel.style.display = 'block';
      panel.innerHTML = renderResult(result, displayText);
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
      // Save to history
      window.ScamPayHistory?.saveToHistory({
        text: displayText,
        score: result.score,
        category: result.category,
        riskLevel: result.riskLevel.level,
        type: scanType,
      });
    }, 1200);
    return;
  }

  // Text/screenshot analysis
  const btn = document.getElementById('scanBtn');
  const btnText = document.getElementById('scanBtnText');
  const spinner = document.getElementById('scanSpinner');
  btn.disabled = true;
  btnText.style.display = 'none';
  spinner.style.display = 'inline-block';

  setTimeout(() => {
    const result = analyzeText(inputText);
    const panel = document.getElementById('resultPanel');
    panel.style.display = 'block';
    panel.innerHTML = renderResult(result, displayText);
    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    btn.disabled = false;
    btnText.style.display = 'inline';
    spinner.style.display = 'none';
    // Save to history
    window.ScamPayHistory?.saveToHistory({
      text: displayText.substring(0, 100),
      score: result.score,
      category: result.category,
      riskLevel: result.riskLevel.level,
      type: scanType,
    });
  }, 1400);
}

// ============================================
// EVENT LISTENERS
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab)?.classList.add('active');
      document.getElementById('resultPanel').style.display = 'none';
    });
  });

  // Sample message buttons
  document.querySelectorAll('.sample-btn[data-msg]').forEach(btn => {
    btn.addEventListener('click', () => {
      const ta = document.getElementById('msgInput');
      if (ta) {
        ta.value = btn.dataset.msg;
        document.getElementById('charCount').textContent = ta.value.length;
      }
    });
  });

  // Sample identifier buttons
  document.querySelectorAll('.sample-btn[data-id]').forEach(btn => {
    btn.addEventListener('click', () => {
      const sel = document.getElementById('idType');
      const inp = document.getElementById('idValue');
      if (sel) sel.value = btn.dataset.id;
      if (inp) inp.value = btn.dataset.val;
    });
  });

  // Char count
  document.getElementById('msgInput')?.addEventListener('input', (e) => {
    document.getElementById('charCount').textContent = e.target.value.length;
  });

  // Scan button
  document.getElementById('scanBtn')?.addEventListener('click', runScan);

  // File upload
  const fileInput = document.getElementById('fileInput');
  const uploadZone = document.getElementById('uploadZone');
  const uploadPreview = document.getElementById('uploadPreview');
  const previewImg = document.getElementById('previewImg');
  const clearImg = document.getElementById('clearImg');

  fileInput?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      previewImg.src = ev.target.result;
      uploadZone.style.display = 'none';
      uploadPreview.style.display = 'flex';
    };
    reader.readAsDataURL(file);
  });

  clearImg?.addEventListener('click', () => {
    fileInput.value = '';
    previewImg.src = '';
    uploadZone.style.display = 'block';
    uploadPreview.style.display = 'none';
  });

  // Drag and drop
  uploadZone?.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragging'); });
  uploadZone?.addEventListener('dragleave', () => uploadZone.classList.remove('dragging'));
  uploadZone?.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragging');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      fileInput.dispatchEvent(new Event('change'));
    }
  });
});
