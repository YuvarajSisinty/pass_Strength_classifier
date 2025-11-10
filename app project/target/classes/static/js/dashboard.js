// Dashboard JavaScript

const API_BASE_URL = 'http://localhost:8080/api';

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }

    // Display username
    const usernameDisplay = document.getElementById('usernameDisplay');
    if (usernameDisplay) {
        usernameDisplay.textContent = getUsername();
    }

    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // Switch to active tab
    function switchTab(tabName) {
        // Update buttons
        tabButtons.forEach(btn => {
            if (btn.getAttribute('data-tab') === tabName) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update content
        document.getElementById('consultationTab').classList.remove('active');
        document.getElementById('historyTab').classList.remove('active');
        
        if (tabName === 'consultation') {
            document.getElementById('consultationTab').classList.add('active');
        } else {
            document.getElementById('historyTab').classList.add('active');
            loadConsultationHistory();
        }
    }

    // Symptom form handler
    const symptomForm = document.getElementById('symptomForm');
    if (symptomForm) {
        symptomForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const symptoms = document.getElementById('symptoms').value;
            const resultContainer = document.getElementById('consultationResult');
            
            try {
                const token = getToken();
                const response = await fetch(`${API_BASE_URL}/consultations/symptoms`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ symptoms })
                });

                if (response.ok) {
                    const data = await response.json();
                    displayConsultationResult(data, 'SYMPTOM');
                    symptomForm.reset();
                    // Refresh history after consultation
                    setTimeout(loadConsultationHistory, 1000);
                } else {
                    const error = await response.json();
                    resultContainer.innerHTML = `<div class="error-message">Error: ${error.message || 'Failed to analyze symptoms'}</div>`;
                    resultContainer.style.display = 'block';
                }
            } catch (error) {
                resultContainer.innerHTML = `<div class="error-message">An error occurred. Please try again.</div>`;
                resultContainer.style.display = 'block';
                console.error('Error:', error);
            }
        });
    }

    // Image form handler
    const imageForm = document.getElementById('imageForm');
    if (imageForm) {
        imageForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('imageFile');
            const file = fileInput.files[0];
            const resultContainer = document.getElementById('consultationResult');
            
            if (!file) {
                alert('Please select an image file');
                return;
            }

            try {
                const token = getToken();
                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch(`${API_BASE_URL}/consultations/image`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    displayConsultationResult(data, 'IMAGE');
                    imageForm.reset();
                    // Refresh history after consultation
                    setTimeout(loadConsultationHistory, 1000);
                } else {
                    const error = await response.json();
                    resultContainer.innerHTML = `<div class="error-message">Error: ${error.message || 'Failed to analyze image'}</div>`;
                    resultContainer.style.display = 'block';
                }
            } catch (error) {
                resultContainer.innerHTML = `<div class="error-message">An error occurred. Please try again.</div>`;
                resultContainer.style.display = 'block';
                console.error('Error:', error);
            }
        });
    }

    // Refresh history button
    const refreshHistory = document.getElementById('refreshHistory');
    if (refreshHistory) {
        refreshHistory.addEventListener('click', loadConsultationHistory);
    }

    // Load history on page load if on history tab
    if (document.getElementById('historyTab').classList.contains('active')) {
        loadConsultationHistory();
    }
});

function displayConsultationResult(data, type) {
    const resultContainer = document.getElementById('consultationResult');
    let html = '<h3>Consultation Result</h3>';
    
    if (type === 'SYMPTOM') {
        html += `<div class="consultation-item">
            <h4>Symptom Analysis</h4>
            <p><strong>Symptoms:</strong> ${data.symptoms || 'N/A'}</p>
            <div class="content">
                <pre>${data.prescriptionSuggestion || 'No prescription suggestion available'}</pre>
            </div>
            <p class="date">Date: ${new Date(data.createdAt).toLocaleString()}</p>
        </div>`;
    } else if (type === 'IMAGE') {
        const seriousnessClass = data.seriousnessRating ? data.seriousnessRating.toLowerCase() : '';
        html += `<div class="consultation-item">
            <h4>Image Analysis</h4>
            ${data.imagePath ? `<p><img src="/${data.imagePath}" alt="Uploaded image" style="max-width: 300px; border-radius: 5px; margin: 10px 0;"></p>` : ''}
            <span class="seriousness-rating ${seriousnessClass}">Seriousness: ${data.seriousnessRating || 'N/A'}</span>
            <div class="content">
                <pre>${data.analysisResult || 'No analysis available'}</pre>
            </div>
            <p class="date">Date: ${new Date(data.createdAt).toLocaleString()}</p>
        </div>`;
    }
    
    resultContainer.innerHTML = html;
    resultContainer.style.display = 'block';
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function loadConsultationHistory() {
    const historyContainer = document.getElementById('historyContainer');
    
    if (!historyContainer) return;
    
    historyContainer.innerHTML = '<p>Loading your consultation history...</p>';
    
    try {
        const token = getToken();
        const response = await fetch(`${API_BASE_URL}/consultations/history`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const consultations = await response.json();
            
            if (consultations.length === 0) {
                historyContainer.innerHTML = '<p>No consultation history found. Start a new consultation to see results here.</p>';
                return;
            }

            let html = '';
            consultations.forEach(consultation => {
                const seriousnessClass = consultation.seriousnessRating ? consultation.seriousnessRating.toLowerCase() : '';
                const typeLabel = consultation.consultationType === 'SYMPTOM' ? 'Symptom Analysis' : 'Image Analysis';
                
                html += `<div class="consultation-item">
                    <h4>${typeLabel}</h4>
                    <span class="consultation-type-badge">${consultation.consultationType}</span>
                    ${consultation.seriousnessRating ? `<span class="seriousness-rating ${seriousnessClass}">${consultation.seriousnessRating}</span>` : ''}
                    <p class="date">${new Date(consultation.createdAt).toLocaleString()}</p>`;
                
                if (consultation.symptoms) {
                    html += `<p><strong>Symptoms:</strong> ${consultation.symptoms}</p>`;
                }
                
                if (consultation.prescriptionSuggestion) {
                    html += `<div class="content">
                        <strong>Prescription Suggestion:</strong>
                        <pre>${consultation.prescriptionSuggestion}</pre>
                    </div>`;
                }
                
                if (consultation.imagePath) {
                    html += `<p><img src="/${consultation.imagePath}" alt="Uploaded image" style="max-width: 300px; border-radius: 5px; margin: 10px 0;"></p>`;
                }
                
                if (consultation.analysisResult) {
                    html += `<div class="content">
                        <strong>Analysis Result:</strong>
                        <pre>${consultation.analysisResult}</pre>
                    </div>`;
                }
                
                html += '</div>';
            });

            historyContainer.innerHTML = html;
        } else {
            if (response.status === 401) {
                // Token expired or invalid
                logout();
            } else {
                historyContainer.innerHTML = '<p class="error-message">Failed to load consultation history. Please try again.</p>';
            }
        }
    } catch (error) {
        historyContainer.innerHTML = '<p class="error-message">An error occurred while loading history. Please try again.</p>';
        console.error('Error:', error);
    }
}

