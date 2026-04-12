// API Configuration
const API_URL = 'http://127.0.0.1:5000/api';

// DOM Elements
const detectBtn = document.getElementById('detect-btn');
const batchDetectBtn = document.getElementById('batch-detect-btn');
const analyzeFeuresBtn = document.getElementById('analyze-features-btn');
const urlInput = document.getElementById('url-input');
const htmlInput = document.getElementById('html-input');
const batchUrlsInput = document.getElementById('batch-urls');
const featureUrlInput = document.getElementById('feature-url');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const resultContent = document.getElementById('result-content');
const batchResultsDiv = document.getElementById('batch-results');
const batchSummary = document.getElementById('batch-summary');
const batchDetail = document.getElementById('batch-detail');
const featuresResultsDiv = document.getElementById('features-results');
const featuresContent = document.getElementById('features-content');
const toast = document.getElementById('toast');

// Tab navigation
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', (e) => {
        const tabName = e.target.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Mark button as active
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Load model info on about tab
    if (tabName === 'about') {
        loadModelInfo();
    }
}

// Show toast notification
function showToast(message, type = 'info', duration = 4000) {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// Single URL Detection
detectBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    const htmlContent = htmlInput.value.trim();
    
    if (!url) {
        showToast('Please enter a URL', 'error');
        return;
    }
    
    await detectPhishing(url, htmlContent);
});

// Allow Enter key in URL input
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        detectBtn.click();
    }
});

async function detectPhishing(url, htmlContent = '') {
    try {
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        
        const response = await fetch(`${API_URL}/detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                html_content: htmlContent
            })
        });
        
        const data = await response.json();
        loadingDiv.classList.add('hidden');
        
        if (!response.ok) {
            showToast(`Error: ${data.error}`, 'error');
            return;
        }
        
        displaySingleResult(data.data);
        resultsDiv.classList.remove('hidden');
        
    } catch (error) {
        loadingDiv.classList.add('hidden');
        showToast(`Network error: ${error.message}`, 'error');
    }
}

function displaySingleResult(result) {
    if (result.error) {
        resultContent.innerHTML = `
            <div class="result-card">
                <p style="color: var(--danger-color);">❌ Error: ${result.error}</p>
            </div>
        `;
        return;
    }
    
    const isPhishing = result.is_phishing;
    const cardClass = isPhishing ? 'phishing' : 'legitimate';
    const labelClass = isPhishing ? 'phishing' : 'legitimate';
    const labelText = isPhishing ? '⚠️ PHISHING DETECTED' : '✅ LEGITIMATE';
    const icon = isPhishing ? '🚨' : '✨';
    
    let html = `
        <div class="result-card ${cardClass}">
            <div class="result-label ${labelClass}">${labelText}</div>
            
            <div class="result-info">
                <div class="result-item">
                    <div class="result-item-label">Confidence</div>
                    <div class="result-item-value">${(result.confidence * 100).toFixed(1)}%</div>
                </div>
                <div class="result-item">
                    <div class="result-item-label">Risk Score</div>
                    <div class="result-item-value">${result.risk_score}</div>
                    <div class="result-score-bar">
                        <div class="result-score-fill ${isPhishing ? 'danger' : 'success'}" 
                             style="width: ${result.risk_score}%"></div>
                    </div>
                </div>
                <div class="result-item">
                    <div class="result-item-label">Legitimate Score</div>
                    <div class="result-item-value">${result.legitimate_score}%</div>
                </div>
                <div class="result-item">
                    <div class="result-item-label">Phishing Score</div>
                    <div class="result-item-value">${result.phishing_score}%</div>
                </div>
            </div>
    `;
    
    // Risk indicators
    if (result.risk_indicators && result.risk_indicators.length > 0) {
        html += `
            <div class="risk-indicators">
                <h4>${icon} Suspicious Indicators Found:</h4>
                <ul class="indicator-list">
        `;
        result.risk_indicators.forEach(indicator => {
            html += `<li class="indicator-item">${indicator}</li>`;
        });
        html += `
                </ul>
            </div>
        `;
    }
    
    html += `</div>`;
    
    resultContent.innerHTML = html;
}

// Batch Detection
batchDetectBtn.addEventListener('click', async () => {
    const urlsText = batchUrlsInput.value.trim();
    
    if (!urlsText) {
        showToast('Please enter at least one URL', 'error');
        return;
    }
    
    const urls = urlsText.split('\n')
        .map(url => url.trim())
        .filter(url => url.length > 0);
    
    if (urls.length === 0) {
        showToast('Please enter at least one valid URL', 'error');
        return;
    }
    
    if (urls.length > 10) {
        showToast('Maximum 10 URLs at a time', 'warning');
        urls.splice(10);
    }
    
    await performBatchDetection(urls);
});

async function performBatchDetection(urls) {
    try {
        loadingDiv.classList.remove('hidden');
        batchResultsDiv.classList.add('hidden');
        
        const response = await fetch(`${API_URL}/batch-detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urls: urls })
        });
        
        const data = await response.json();
        loadingDiv.classList.add('hidden');
        
        if (!response.ok) {
            showToast(`Error: ${data.error}`, 'error');
            return;
        }
        
        displayBatchResults(data.data);
        batchResultsDiv.classList.remove('hidden');
        showToast(`Analyzed ${data.count} URLs`, 'success');
        
    } catch (error) {
        loadingDiv.classList.add('hidden');
        showToast(`Network error: ${error.message}`, 'error');
    }
}

function displayBatchResults(results) {
    let phishingCount = 0;
    let legitimateCount = 0;
    let errorCount = 0;
    
    results.forEach(result => {
        if (result.error) {
            errorCount++;
        } else if (result.is_phishing) {
            phishingCount++;
        } else {
            legitimateCount++;
        }
    });
    
    // Summary
    batchSummary.innerHTML = `
        <div class="summary-item" style="border-left: 4px solid var(--danger-color);">
            <div class="summary-count" style="color: var(--danger-color)">${phishingCount}</div>
            <div class="summary-label">Phishing Detected</div>
        </div>
        <div class="summary-item" style="border-left: 4px solid var(--success-color);">
            <div class="summary-count" style="color: var(--success-color)">${legitimateCount}</div>
            <div class="summary-label">Legitimate</div>
        </div>
        <div class="summary-item" style="border-left: 4px solid var(--text-secondary);">
            <div class="summary-count" style="color: var(--text-secondary)">${errorCount}</div>
            <div class="summary-label">Errors</div>
        </div>
    `;
    
    // Details
    let detailHtml = '<h4>Detailed Results:</h4>';
    results.forEach((result, index) => {
        let status = 'Unknown';
        let statusClass = '';
        
        if (result.error) {
            status = 'Error';
            statusClass = 'error';
        } else if (result.is_phishing) {
            status = '⚠️ Phishing';
            statusClass = 'phishing';
        } else {
            status = '✅ Legitimate';
            statusClass = 'legitimate';
        }
        
        detailHtml += `
            <div class="batch-item">
                <div class="batch-url">
                    <strong>${index + 1}.</strong> ${result.url}
                </div>
                <div class="batch-status ${statusClass}">${status}</div>
            </div>
        `;
    });
    
    batchDetail.innerHTML = detailHtml;
}

// Feature Analysis
document.getElementById('analyze-features-btn').addEventListener('click', async () => {
    const url = featureUrlInput.value.trim();
    
    if (!url) {
        showToast('Please enter a URL', 'error');
        return;
    }
    
    await extractFeatures(url);
});

featureUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('analyze-features-btn').click();
    }
});

async function extractFeatures(url) {
    try {
        loadingDiv.classList.remove('hidden');
        featuresResultsDiv.classList.add('hidden');
        
        const response = await fetch(`${API_URL}/analyze-features`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        loadingDiv.classList.add('hidden');
        
        if (!response.ok) {
            showToast(`Error: ${data.error}`, 'error');
            return;
        }
        
        displayFeatures(data.features);
        featuresResultsDiv.classList.remove('hidden');
        
    } catch (error) {
        loadingDiv.classList.add('hidden');
        showToast(`Network error: ${error.message}`, 'error');
    }
}

function displayFeatures(features) {
    let html = '<table class="features-table"><thead><tr><th>Feature</th><th>Value</th></tr></thead><tbody>';
    
    // Group features by type
    const urlFeatures = {};
    const htmlFeatures = {};
    
    for (const [key, value] of Object.entries(features)) {
        if (['has_https', 'has_ip_address', 'has_at_symbol', 'has_hyphen_in_domain', 
              'has_unusual_port', 'common_tld', 'url_length', 'domain_length', 
              'num_dots_in_domain', 'url_entropy', 'has_redirect_chars', 
              'special_chars_in_url', 'subdomain_count', 'num_query_params'].includes(key)) {
            urlFeatures[key] = value;
        } else {
            htmlFeatures[key] = value;
        }
    }
    
    // URL Features
    if (Object.keys(urlFeatures).length > 0) {
        html += '<tr style="background-color: var(--primary-color); color: white;"><td colspan="2"><strong>URL Features</strong></td></tr>';
        for (const [key, value] of Object.entries(urlFeatures)) {
            html += formatFeatureRow(key, value);
        }
    }
    
    // HTML Features
    if (Object.keys(htmlFeatures).length > 0) {
        html += '<tr style="background-color: var(--warning-color); color: white;"><td colspan="2"><strong>HTML Features</strong></td></tr>';
        for (const [key, value] of Object.entries(htmlFeatures)) {
            html += formatFeatureRow(key, value);
        }
    }
    
    html += '</tbody></table>';
    
    featuresContent.innerHTML = html;
}

function formatFeatureRow(key, value) {
    const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    let displayValue = value;
    
    if (typeof value === 'number') {
        displayValue = value.toFixed(3);
    } else if (typeof value === 'boolean') {
        displayValue = value ? '✓' : '✗';
    }
    
    return `<tr><td>${displayKey}</td><td class="feature-value">${displayValue}</td></tr>`;
}

// Load Model Info
async function loadModelInfo() {
    const modelInfoDiv = document.getElementById('model-info-div');
    
    try {
        const response = await fetch(`${API_URL}/model-info`);
        const data = await response.json();
        
        if (!response.ok) {
            modelInfoDiv.innerHTML = '<p>Could not load model information</p>';
            return;
        }
        
        let html = '<div class="model-info">';
        html += `<div class="model-info-item">
                    <span class="model-info-label">Model Type:</span>
                    <span class="model-info-value">${data.model_type}</span>
                </div>`;
        html += `<div class="model-info-item">
                    <span class="model-info-label">Trees/Estimators:</span>
                    <span class="model-info-value">${data.n_estimators}</span>
                </div>`;
        html += `<div class="model-info-item">
                    <span class="model-info-label">Features Count:</span>
                    <span class="model-info-value">${data.features_count}</span>
                </div>`;
        html += '</div>';
        
        modelInfoDiv.innerHTML = html;
    } catch (error) {
        modelInfoDiv.innerHTML = '<p>Error loading model information</p>';
    }
}

// Health check on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✓ Backend connected successfully');
        }
    } catch (error) {
        console.error('✗ Unable to connect to backend:', error);
        showToast('⚠️ Backend server not running. Make sure Flask app is started!', 'error', 6000);
    }
});
