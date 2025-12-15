// web/app.js - FIXED VERSION

let currentResults = null;

async function processCourse() {
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();
    const scope = document.getElementById('scope').value.trim();
    const duration = document.getElementById('duration').value.trim();
    
    if (!title || !description || !scope || !duration) {
        alert('Please fill in all fields');
        return;
    }
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('submitBtn').disabled = true;
    
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description, scope, duration })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Processing failed');
        }
        
        const results = await response.json();
        currentResults = results;
        
        displayResults(results);
        
        // Hide form, show results
        document.getElementById('inputForm').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');
        
    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Full error:', error);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('submitBtn').disabled = false;
    }
}

function displayResults(results) {
    // Update header
    document.getElementById('resultTitle').textContent = results.metadata.courseTitle;
    document.getElementById('resultDate').textContent = 'Generated: ' + results.metadata.generated_date;
    
    // Update quality score
    const qualityScore = results.assessmentAnalysis?.quality_score || 0;
    const qualityGrade = results.assessmentAnalysis?.overall_grade || 'N/A';
    document.getElementById('qualityScore').textContent = qualityScore.toFixed(1);
    document.getElementById('qualityGrade').textContent = qualityGrade;
    
    // Update stats
    document.getElementById('statModules').textContent = results.modules?.length || 0;
    document.getElementById('statOutcomes').textContent = results.courseLearningOutcomes?.length || 0;
    document.getElementById('statQuestions').textContent = results.sampleQuestions?.length || 0;
    document.getElementById('statHours').textContent = (results.totalHours || 0) + 'h';
    
    // Show overview tab by default
    showTab('overview', null);
}

function showTab(tabName, event) {
    // Update button styles
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('tab-active', 'text-indigo-600');
        btn.classList.add('text-gray-600');
    });
    
    // If event exists, highlight the clicked button
    if (event && event.target) {
        event.target.classList.add('tab-active', 'text-indigo-600');
        event.target.classList.remove('text-gray-600');
    } else {
        // If no event (called programmatically), find and highlight by tab name
        const buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(btn => {
            if (btn.textContent.toLowerCase() === tabName) {
                btn.classList.add('tab-active', 'text-indigo-600');
                btn.classList.remove('text-gray-600');
            }
        });
    }
    
    const content = document.getElementById('tabContent');
    
    if (!currentResults) {
        content.innerHTML = '<p class="text-gray-500">No data available</p>';
        return;
    }
    
    switch(tabName) {
        case 'overview':
            content.innerHTML = generateOverviewTab();
            break;
        case 'modules':
            content.innerHTML = generateModulesTab();
            break;
        case 'outcomes':
            content.innerHTML = generateOutcomesTab();
            break;
        case 'assessment':
            content.innerHTML = generateAssessmentTab();
            break;
        case 'questions':
            content.innerHTML = generateQuestionsTab();
            break;
        case 'alignment':
            content.innerHTML = generateAlignmentTab();
            break;
        default:
            content.innerHTML = '<p class="text-gray-500">Invalid tab</p>';
    }
}

function generateOverviewTab() {
    if (!currentResults || !currentResults.bloomStatistics) {
        return '<p class="text-gray-500">No statistics available</p>';
    }
    
    const stats = currentResults.bloomStatistics.module_level.percentages;
    let html = '<div class="space-y-6">';
    html += '<h3 class="text-xl font-bold text-gray-800 mb-4">Bloom\'s Taxonomy Distribution</h3>';
    html += '<div class="space-y-2">';
    
    const bloomLevels = ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create'];
    for (const level of bloomLevels) {
        const pct = stats[level] || 0;
        html += `
            <div>
                <div class="flex justify-between text-sm mb-1">
                    <span class="font-medium text-gray-700">${level}</span>
                    <span class="text-gray-600">${pct}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full" style="width: ${pct}%"></div>
                </div>
            </div>
        `;
    }
    
    html += '</div></div>';
    return html;
}

function generateModulesTab() {
    if (!currentResults || !currentResults.modules) {
        return '<p class="text-gray-500">No modules available</p>';
    }
    
    let html = '<div class="space-y-4">';
    
    currentResults.modules.forEach(module => {
        html += `
            <div class="border border-gray-200 rounded-lg p-4">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="text-lg font-bold text-gray-800">Module ${module.id}: ${module.title}</h4>
                    <span class="text-sm bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full">${module.hours}h</span>
                </div>
                <p class="text-gray-600 text-sm mb-2">${module.description || ''}</p>
                <div class="flex flex-wrap gap-2 mb-2">
                    ${(module.subtopics || []).map(st => `<span class="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">${st}</span>`).join('')}
                </div>
                <div class="text-sm">
                    ${(module.learningOutcomes || []).map(lo => `
                        <div class="flex items-start gap-2 mb-1">
                            <svg class="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-700">${lo.outcome} <span class="text-indigo-600 font-medium">[${lo.bloomLevel}]</span></span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function generateOutcomesTab() {
    if (!currentResults || !currentResults.courseLearningOutcomes) {
        return '<p class="text-gray-500">No outcomes available</p>';
    }
    
    let html = '<div class="space-y-3">';
    
    currentResults.courseLearningOutcomes.forEach(outcome => {
        html += `
            <div class="bg-indigo-50 rounded-lg p-4">
                <div class="flex justify-between mb-2">
                    <span class="font-semibold text-indigo-900">${outcome.id}</span>
                    <span class="text-sm bg-indigo-200 text-indigo-800 px-2 py-1 rounded">${outcome.bloomLevel}</span>
                </div>
                <p class="text-gray-800 text-sm">${outcome.outcome}</p>
                <p class="text-xs text-gray-600 mt-2">Mapped to modules: ${(outcome.mappedModules || []).join(', ') || 'None'}</p>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function generateAssessmentTab() {
    if (!currentResults || !currentResults.assessmentBlueprint || !currentResults.assessmentBlueprint.components) {
        return '<p class="text-gray-500">No assessment data available</p>';
    }
    
    let html = '<div class="space-y-3">';
    
    currentResults.assessmentBlueprint.components.forEach(comp => {
        html += `
            <div class="bg-purple-50 rounded-lg p-4">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="font-bold text-purple-900">${comp.type}</h4>
                    <span class="text-xl font-bold text-purple-600">${comp.weight}%</span>
                </div>
                <p class="text-gray-700 text-sm mb-2">${comp.description}</p>
                <div class="text-xs text-gray-600">
                    <div>Timing: ${comp.timing}</div>
                    <div>Bloom Levels: ${(comp.bloomLevels || []).join(', ')}</div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function generateQuestionsTab() {
    if (!currentResults || !currentResults.sampleQuestions) {
        return '<p class="text-gray-500">No questions available</p>';
    }
    
    let html = '<div class="space-y-3">';
    
    currentResults.sampleQuestions.forEach(q => {
        html += `
            <div class="border border-gray-200 rounded-lg p-3">
                <div class="flex gap-2 mb-2 flex-wrap">
                    <span class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">Module ${q.moduleId}</span>
                    <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">${q.type}</span>
                    <span class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">${q.bloomLevel}</span>
                    <span class="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded">${q.difficulty}</span>
                </div>
                <p class="text-gray-800 text-sm">${q.question}</p>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function generateAlignmentTab() {
    if (!currentResults || !currentResults.alignmentMatrix) {
        return '<p class="text-gray-500">No alignment data available</p>';
    }
    
    let html = '<div class="space-y-3">';
    
    currentResults.alignmentMatrix.forEach(row => {
        html += `
            <div class="border border-gray-200 rounded-lg p-3">
                <div class="text-sm font-semibold text-gray-800 mb-1">${row.module}</div>
                <div class="text-sm text-gray-600 mb-2">${row.learningOutcome}</div>
                <div class="flex gap-2 flex-wrap">
                    <span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">${row.coverage}</span>
                    <span class="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded">${row.bloomLevel}</span>
                </div>
                <div class="text-xs text-gray-500 mt-2">
                    <div>Assessments: ${(row.assessmentTypes || []).join(', ') || 'None'}</div>
                    <div>Questions: ${(row.questionIds || []).slice(0, 3).join(', ') || 'None'}</div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function downloadJSON() {
    if (!currentResults) {
        alert('No data to download');
        return;
    }
    
    const dataStr = JSON.stringify(currentResults, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'syllabus_results.json';
    a.click();
    URL.revokeObjectURL(url);
}

function downloadCSV() {
    if (!currentResults || !currentResults.alignmentMatrix) {
        alert('No alignment data to download');
        return;
    }
    
    let csv = 'Module,Learning Outcome,Bloom Level,Assessment Types,Question IDs,Coverage\n';
    currentResults.alignmentMatrix.forEach(row => {
        const assessments = (row.assessmentTypes || []).join('; ');
        const questions = (row.questionIds || []).join('; ');
        csv += `"${row.module}","${row.learningOutcome}","${row.bloomLevel}","${assessments}","${questions}","${row.coverage}"\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'alignment_matrix.csv';
    a.click();
    URL.revokeObjectURL(url);
}

function downloadReport() {
    if (!currentResults) {
        alert('No data to download');
        return;
    }
    
    let report = `SYLLABUS EXPANSION REPORT\n`;
    report += `${'='.repeat(80)}\n\n`;
    report += `Course: ${currentResults.metadata.courseTitle}\n`;
    report += `Generated: ${currentResults.metadata.generated_date}\n`;
    report += `Type: ${currentResults.courseType}\n`;
    report += `Duration: ${currentResults.metadata.duration}\n`;
    report += `Total Hours: ${currentResults.totalHours}\n\n`;
    report += `${'='.repeat(80)}\n`;
    report += `MODULES\n`;
    report += `${'='.repeat(80)}\n\n`;
    
    (currentResults.modules || []).forEach(module => {
        report += `Module ${module.id}: ${module.title} (${module.hours}h)\n`;
        report += `Subtopics: ${(module.subtopics || []).join(', ')}\n`;
        report += `Learning Outcomes:\n`;
        (module.learningOutcomes || []).forEach(lo => {
            report += `  - ${lo.outcome} [${lo.bloomLevel}]\n`;
        });
        report += `\n`;
    });
    
    report += `${'='.repeat(80)}\n`;
    report += `ASSESSMENT BLUEPRINT\n`;
    report += `${'='.repeat(80)}\n\n`;
    
    (currentResults.assessmentBlueprint?.components || []).forEach(comp => {
        report += `${comp.type}: ${comp.weight}%\n`;
        report += `  ${comp.description}\n`;
        report += `  Timing: ${comp.timing}\n\n`;
    });
    
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'syllabus_report.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function resetForm() {
    document.getElementById('inputForm').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('title').value = '';
    document.getElementById('description').value = '';
    document.getElementById('scope').value = '';
    document.getElementById('duration').value = '';
    currentResults = null;
}