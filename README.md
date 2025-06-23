<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Energy Calculator</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary-orange: #F87B45;
            --primary-orange-light: #FF9C6E;
            --primary-orange-dark: #E65A28;
            --success-green: #10b981;
            --background-light: #fef7f0;
            --background-white: #ffffff;
            --text-dark: #1f2937;
            --text-medium: #4b5563;
            --text-light: #6b7280;
            --border-light: #e5e7eb;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, var(--background-light) 0%, #fff 100%);
            color: var(--text-dark);
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-orange) 0%, var(--primary-orange-dark) 100%);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 40px;
            color: white;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 12px;
        }
        
        .header p {
            font-size: 1.125rem;
            opacity: 0.95;
        }
        
        .input-section {
            background: var(--background-white);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 24px;
            color: var(--text-dark);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-title .icon {
            color: var(--primary-orange);
            width: 24px;
            height: 24px;
        }
        
        .grid {
            display: grid;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .grid-2 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .grid-3 {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-dark);
        }
        
        .form-input, .form-select {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid var(--border-light);
            border-radius: 8px;
            font-size: 14px;
            background: var(--background-white);
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: var(--primary-orange);
            box-shadow: 0 0 0 4px rgba(248, 123, 69, 0.1);
        }
        
        .form-input:disabled {
            background-color: #f9fafb;
            color: var(--text-light);
            border-color: #e5e7eb;
        }
        
        .file-input {
            display: block;
            width: 100%;
            font-size: 14px;
            color: var(--text-medium);
            padding: 16px;
            border: 2px dashed var(--primary-orange);
            border-radius: 12px;
            background: rgba(248, 123, 69, 0.02);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .file-input:hover {
            background: rgba(248, 123, 69, 0.05);
            border-color: var(--primary-orange-dark);
        }
        
        .rate-info {
            background: linear-gradient(135deg, rgba(248, 123, 69, 0.05) 0%, rgba(248, 123, 69, 0.02) 100%);
            padding: 20px;
            border-radius: 12px;
            margin-top: 16px;
            border: 1px solid rgba(248, 123, 69, 0.2);
        }
        
        .rate-info p {
            font-size: 14px;
            margin-bottom: 8px;
            color: var(--text-dark);
        }
        
        .rate-info p:last-child {
            font-size: 12px;
            color: var(--text-medium);
            margin-bottom: 0;
        }
        
        .calculate-btn {
            width: 100%;
            padding: 20px 32px;
            background: linear-gradient(135deg, var(--primary-orange) 0%, var(--primary-orange-dark) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 30px 0;
        }
        
        .calculate-btn:hover {
            background: linear-gradient(135deg, var(--primary-orange-dark) 0%, #d4461a 100%);
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        }
        
        .results-section {
            background: var(--background-white);
            border-radius: 16px;
            padding: 40px;
            margin-top: 30px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            display: none;
        }
        
        .results-section.show {
            display: block;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }
        
        .result-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(248, 123, 69, 0.1);
        }
        
        .result-item:last-child {
            border-bottom: none;
        }
        
        .result-item.total {
            border-top: 2px solid var(--primary-orange);
            padding: 20px;
            background: rgba(248, 123, 69, 0.05);
            border-radius: 8px;
            margin-top: 16px;
            font-weight: 700;
        }
        
        .result-value {
            font-weight: 600;
            font-size: 16px;
        }
        
        .result-value.positive {
            color: var(--success-green);
        }
        
        .result-value.large {
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary-orange);
        }
        
        .environmental-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        .env-card {
            text-align: center;
            padding: 32px 24px;
            border-radius: 16px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .env-card:hover {
            transform: translateY(-4px);
        }
        
        .env-card.green {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
            border-color: rgba(16, 185, 129, 0.2);
        }
        
        .env-card.orange {
            background: linear-gradient(135deg, rgba(248, 123, 69, 0.1) 0%, rgba(248, 123, 69, 0.05) 100%);
            border-color: rgba(248, 123, 69, 0.2);
        }
        
        .env-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 8px;
            line-height: 1;
        }
        
        .env-value.green {
            color: var(--success-green);
        }
        
        .env-value.orange {
            color: var(--primary-orange);
        }
        
        .env-label {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .env-label.green {
            color: #065f46;
        }
        
        .env-label.orange {
            color: #c2410c;
        }
        
        .success-message {
            color: var(--success-green);
            font-size: 14px;
            margin-bottom: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .success-message:before {
            content: "✓";
            background: var(--success-green);
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }
        
        .table-container {
            overflow-x: auto;
            margin-top: 20px;
            border-radius: 12px;
        }
        
        .data-table {
            width: 100%;
            font-size: 12px;
            border-collapse: collapse;
            background: var(--background-white);
        }
        
        .data-table th,
        .data-table td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-light);
        }
        
        .data-table th {
            background: linear-gradient(90deg, var(--primary-orange) 0%, var(--primary-orange-light) 100%);
            color: white;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 11px;
        }
        
        .data-table tr:hover {
            background: rgba(248, 123, 69, 0.02);
        }
        
        .icon {
            width: 20px;
            height: 20px;
            stroke: currentColor;
            fill: none;
            stroke-width: 2;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header {
                padding: 30px 24px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .input-section {
                padding: 24px;
            }
            
            .results-grid,
            .environmental-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .env-value {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Solar Energy Calculator</h1>
            <p>Calculate solar energy savings based on consumption data and utility rates</p>
        </div>

        <div class="input-section">
            <div class="section-title">
                <svg class="icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7,10 12,15 17,10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                CSV Data Upload (Optional)
            </div>
            <input type="file" id="csvFile" accept=".csv" class="file-input">
            <div id="csvPreview"></div>

            <div class="section-title">
                <svg class="icon" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                Rate Schedule Selection
            </div>
            
            <div class="form-group">
                <label class="form-label">Select Utility Rate Schedule</label>
                <select id="rateSchedule" class="form-select">
                    <option value="PG&E E-TOU-C-NEM2">PG&E - E-TOU-C-NEM2 (Time of Use - Rate C)</option>
                    <option value="PG&E E-TOU-C-NEM2 + CCA V2">PG&E - E-TOU-C-NEM2 + CCA V2 (Rate C with CCA)</option>
                    <option value="PG&E E-TOU-D-NEM2" selected>PG&E - E-TOU-D-NEM2 (Time of Use - Rate D)</option>
                    <option value="PG&E E-TOU-D-NEM2 + CCA">PG&E - E-TOU-D-NEM2 + CCA (Rate D with CCA)</option>
                    <option value="SCE TOU-D-4-9PM-NEM2">SCE - TOU-D-4-9PM-NEM2 (Time of Use - 4-9PM Peak)</option>
                    <option value="SCE TOU-D-5-8PM-NEM2">SCE - TOU-D-5-8PM-NEM2 (Time of Use - 5-8PM Peak)</option>
                    <option value="Custom Rate">Custom Rate Structure</option>
                </select>
                
                <div id="rateInfo" class="rate-info">
                    <p id="rateName"><strong>PG&E E-TOU-D-NEM2 (Time of Use - Rate D)</strong></p>
                    <p id="rateDescription">Standard residential TOU rate with shorter peak window</p>
                    <p id="rateStructure">On-Peak: 5pm-8pm Weekdays | Off-Peak: All other hours</p>
                </div>
            </div>

            <div class="grid grid-2" id="rateInputs">
                <div class="form-group">
                    <label class="form-label">On-Peak Rate ($/kWh)</label>
                    <input type="number" id="onPeakRate" step="0.0001" value="0.48189" class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">Off-Peak Rate ($/kWh)</label>
                    <input type="number" id="offPeakRate" step="0.0001" value="0.44328" class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">Baseline Credit ($/kWh)</label>
                    <input type="number" id="baselineCredit" step="0.00001" value="0.10301" class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">Solar Discount (%)</label>
                    <input type="number" id="solarDiscount" step="0.001" value="7.5" class="form-input">
                </div>
            </div>

            <div class="section-title">
                <svg class="icon" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                Consumption Data
            </div>
            <div class="grid grid-3">
                <div class="form-group">
                    <label class="form-label">On-Peak Usage (kWh)</label>
                    <input type="number" id="onPeakUsage" step="0.001" value="6.333" class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">Off-Peak Usage (kWh)</label>
                    <input type="number" id="offPeakUsage" step="0.001" value="126.074" class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">Baseline Credit (kWh)</label>
                    <input type="number" id="baselineCreditUsage" step="0.001" value="132.407" class="form-input">
                </div>
            </div>

            <div class="section-title">
                <svg class="icon" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><path d="M20 8v6"></path><path d="M23 11h-6"></path></svg>
                Customer Information
            </div>
            <div class="form-group">
                <label class="form-label">CARE Program Eligibility</label>
                <select id="careStatus" class="form-select">
                    <option value="false">Not on CARE Program</option>
                    <option value="true">CARE Program Customer</option>
                </select>
                <div id="careInfo" class="rate-info" style="display: none;">
                    <p id="careDiscount"><strong>CARE Discount Applied</strong></p>
                    <p id="careDescription">CARE customers receive significant discounts on their electricity bills</p>
                    <p id="careDiscountRate">Discount rate varies by utility: PG&E (34.96%), SCE (32.5%)</p>
                </div>
            </div>

            <button id="calculateBtn" class="calculate-btn">
                Calculate Solar Savings
            </button>
        </div>

        <div class="results-section" id="resultsSection">
            <div class="section-title">
                <svg class="icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14,2 14,8 20,8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10,9 9,9 8,9"></polyline></svg>
                <span id="resultsTitle">Solar Energy Calculation Results</span>
            </div>
            <div id="resultsContent"></div>

            <div class="section-title">
                <svg class="icon" viewBox="0 0 24 24"><path d="M7 14l3-3 3 3 5-5"></path></svg>
                Environmental Impact
            </div>
            <div class="environmental-grid" id="environmentalResults"></div>
        </div>
    </div>

    <script>
        // Rate schedules data extracted from Excel files - All 6 rate schedules
        const predefinedRates = {
            'PG&E E-TOU-C-NEM2': {
                name: 'PG&E E-TOU-C-NEM2 (Time of Use - Rate C)',
                utility: 'PG&E',
                onPeakRate: 0.50085,
                offPeakRate: 0.47085,
                baselineCredit: 0.10301,
                solarDiscount: 7.5,
                timeStructure: 'On-Peak: 4pm-9pm Weekdays | Off-Peak: All other hours',
                description: 'Standard residential TOU rate C without CCA'
            },
            'PG&E E-TOU-C-NEM2 + CCA V2': {
                name: 'PG&E E-TOU-C-NEM2 + CCA V2 (Time of Use - Rate C with CCA)',
                utility: 'PG&E',
                onPeakRate: 0.49313,
                offPeakRate: 0.46313,
                baselineCredit: 0.10135,
                solarDiscount: 7.5,
                timeStructure: 'On-Peak: 4pm-9pm Weekdays | Off-Peak: All other hours',
                description: 'Residential TOU rate C with Community Choice Aggregation'
            },
            'PG&E E-TOU-D-NEM2': {
                name: 'PG&E E-TOU-D-NEM2 (Time of Use - Rate D)',
                utility: 'PG&E',
                onPeakRate: 0.48189,
                offPeakRate: 0.44328,
                baselineCredit: 0.10301,
                solarDiscount: 7.5,
                timeStructure: 'On-Peak: 5pm-8pm Weekdays | Off-Peak: All other hours',
                description: 'Standard residential TOU rate D without CCA'
            },
            'PG&E E-TOU-D-NEM2 + CCA': {
                name: 'PG&E E-TOU-D-NEM2 + CCA (Time of Use - Rate D with CCA)',
                utility: 'PG&E',
                onPeakRate: 0.47417,
                offPeakRate: 0.43556,
                baselineCredit: 0.10135,
                solarDiscount: 7.5,
                timeStructure: 'On-Peak: 5pm-8pm Weekdays | Off-Peak: All other hours',
                description: 'Residential TOU rate D with Community Choice Aggregation'
            },
            'SCE TOU-D-4-9PM-NEM2': {
                name: 'SCE TOU-D-4-9PM-NEM2 (Time of Use - Residential)',
                utility: 'SCE',
                midPeakRate: 0.48241,
                offPeakRate: 0.32487,
                superOffPeakRate: 0.28820,
                baselineCredit: 0.09444,
                solarDiscount: 7.5,
                timeStructure: 'Mid-Peak: 4pm-9pm | Off-Peak: 9pm-8am | Super Off-Peak: 8am-4pm',
                description: 'Three-tier time-of-use rate with 4-9pm peak'
            },
            'SCE TOU-D-5-8PM-NEM2': {
                name: 'SCE TOU-D-5-8PM-NEM2 (Time of Use - Residential)',
                utility: 'SCE',
                onPeakRate: 0.46000,
                offPeakRate: 0.31000,
                baselineCredit: 0.09444,
                solarDiscount: 7.5,
                timeStructure: 'On-Peak: 5pm-8pm | Off-Peak: All other hours',
                description: 'Two-tier time-of-use rate with 5-8pm peak'
            },
            'Custom Rate': {
                name: 'Custom Rate Structure',
                utility: 'Custom',
                onPeakRate: 0.45,
                offPeakRate: 0.35,
                baselineCredit: 0.08,
                solarDiscount: 7.5,
                timeStructure: 'User Defined',
                description: 'Manually configurable rate structure'
            }
        };

        // CARE program data
        const CARE_DISCOUNTS = {
            'PG&E': 0.34964,  // 34.964% discount
            'SCE': 0.325       // 32.5% discount
        };

        // Global state
        let csvData = [];
        let calculations = {};
        let currentRates = predefinedRates['PG&E E-TOU-D-NEM2'];
        let isCareCustomer = false;

        // Initialize the application
        function init() {
            setupEventListeners();
            updateRateDisplay();
        }

        // Setup event listeners
        function setupEventListeners() {
            // CSV file upload
            document.getElementById('csvFile').addEventListener('change', handleFileUpload);

            // Rate schedule change
            document.getElementById('rateSchedule').addEventListener('change', handleRateScheduleChange);

            // CARE status change
            document.getElementById('careStatus').addEventListener('change', handleCareStatusChange);

            // Calculate button
            document.getElementById('calculateBtn').addEventListener('click', calculateSolarSavings);
        }

        // Handle CSV file upload
        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file || file.type !== 'text/csv') return;

            const reader = new FileReader();
            reader.onload = (e) => {
                const text = e.target.result;
                const parsed = Papa.parse(text, {
                    header: true,
                    dynamicTyping: true,
                    skipEmptyLines: true
                });
                
                csvData = parsed.data;
                displayCSVPreview();
                
                // Auto-populate with first row if available
                if (csvData.length > 0) {
                    populateFromCSVRow(csvData[0]);
                }
            };
            reader.readAsText(file);
        }

        // Populate inputs from CSV row
        function populateFromCSVRow(row) {
            // Map CSV fields to input elements
            const onPeakUsageEl = document.getElementById('onPeakUsage');
            const offPeakUsageEl = document.getElementById('offPeakUsage');
            const baselineCreditUsageEl = document.getElementById('baselineCreditUsage');
            
            if (onPeakUsageEl && row.on_peak_usage !== undefined) {
                onPeakUsageEl.value = row.on_peak_usage;
            }
            if (offPeakUsageEl && row.off_peak_usage !== undefined) {
                offPeakUsageEl.value = row.off_peak_usage;
            }
            if (baselineCreditUsageEl && row.baseline_credit !== undefined) {
                baselineCreditUsageEl.value = row.baseline_credit;
            }
            
            // Update rate schedule if specified in CSV
            if (row.tariff_code && row.utility) {
                const rateScheduleEl = document.getElementById('rateSchedule');
                if (rateScheduleEl) {
                    // Map tariff codes to our rate schedule keys
                    const tariffMap = {
                        'E-TOU-C-NEM2': 'PG&E E-TOU-C-NEM2',
                        'E-TOU-C-NEM2 + CCA V2': 'PG&E E-TOU-C-NEM2 + CCA V2',
                        'E-TOU-D-NEM2': 'PG&E E-TOU-D-NEM2',
                        'E-TOU-D-NEM2 + CCA': 'PG&E E-TOU-D-NEM2 + CCA',
                        'TOU-D-4-9PM-NEM2': 'SCE TOU-D-4-9PM-NEM2',
                        'TOU-D-5-8PM-NEM2': 'SCE TOU-D-5-8PM-NEM2'
                    };
                    
                    const mappedKey = tariffMap[row.tariff_code];
                    if (mappedKey && predefinedRates[mappedKey]) {
                        rateScheduleEl.value = mappedKey;
                        handleRateScheduleChange();
                    }
                }
            }

            // Update CARE status if specified in CSV
            if (row.is_care !== undefined) {
                const careStatusEl = document.getElementById('careStatus');
                if (careStatusEl) {
                    careStatusEl.value = row.is_care.toString();
                    handleCareStatusChange();
                }
            }
        }

        // Display CSV preview
        function displayCSVPreview() {
            if (csvData.length === 0) return;

            const preview = `
                <div class="success-message">CSV loaded with ${csvData.length} rows</div>
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                ${Object.keys(csvData[0]).map(header => `<th>${header}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${csvData.slice(0, 3).map(row => `
                                <tr>
                                    ${Object.values(row).map(value => `<td>${value || ''}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            document.getElementById('csvPreview').innerHTML = preview;
        }

        // Handle rate schedule change
        function handleRateScheduleChange() {
            const selectedKey = document.getElementById('rateSchedule').value;
            currentRates = predefinedRates[selectedKey];
            updateRateDisplay();
            updateRateInputs();
        }

        // Update rate display information
        function updateRateDisplay() {
            document.getElementById('rateName').innerHTML = `<strong>${currentRates.name}</strong>`;
            document.getElementById('rateDescription').textContent = currentRates.description;
            document.getElementById('rateStructure').textContent = currentRates.timeStructure;
        }

        // Update rate input fields
        function updateRateInputs() {
            const isCustom = document.getElementById('rateSchedule').value === 'Custom Rate';
            const isThreeTier = currentRates.midPeakRate !== undefined;
            const rateInputsEl = document.getElementById('rateInputs');

            // Clear and rebuild rate inputs
            rateInputsEl.innerHTML = '';

            if (isThreeTier) {
                rateInputsEl.innerHTML = `
                    <div class="form-group">
                        <label class="form-label">Mid-Peak Rate ($/kWh)</label>
                        <input type="number" id="midPeakRate" step="0.0001" value="${currentRates.midPeakRate}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Off-Peak Rate ($/kWh)</label>
                        <input type="number" id="offPeakRate" step="0.0001" value="${currentRates.offPeakRate}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Super Off-Peak Rate ($/kWh)</label>
                        <input type="number" id="superOffPeakRate" step="0.0001" value="${currentRates.superOffPeakRate}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Baseline Credit ($/kWh)</label>
                        <input type="number" id="baselineCredit" step="0.00001" value="${currentRates.baselineCredit}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Solar Discount (%)</label>
                        <input type="number" id="solarDiscount" step="0.1" value="${currentRates.solarDiscount}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                `;
            } else {
                rateInputsEl.innerHTML = `
                    <div class="form-group">
                        <label class="form-label">On-Peak Rate ($/kWh)</label>
                        <input type="number" id="onPeakRate" step="0.0001" value="${currentRates.onPeakRate}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Off-Peak Rate ($/kWh)</label>
                        <input type="number" id="offPeakRate" step="0.0001" value="${currentRates.offPeakRate}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Baseline Credit ($/kWh)</label>
                        <input type="number" id="baselineCredit" step="0.00001" value="${currentRates.baselineCredit}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Solar Discount (%)</label>
                        <input type="number" id="solarDiscount" step="0.1" value="${currentRates.solarDiscount}" class="form-input" ${!isCustom ? 'disabled' : ''}>
                    </div>
                `;
            }
        }

        // Handle CARE status change
        function handleCareStatusChange() {
            const careStatus = document.getElementById('careStatus').value === 'true';
            const careInfo = document.getElementById('careInfo');
            
            isCareCustomer = careStatus;
            
            if (careStatus) {
                careInfo.style.display = 'block';
                const utility = currentRates.utility;
                const discountRate = CARE_DISCOUNTS[utility] * 100;
                document.getElementById('careDiscountRate').textContent = 
                    `Current discount: ${utility} customers receive ${discountRate.toFixed(2)}% discount`;
            } else {
                careInfo.style.display = 'none';
            }
        }

        // Get current rates from inputs
        function getCurrentRates() {
            const midPeakInput = document.getElementById('midPeakRate');
            const onPeakInput = document.getElementById('onPeakRate');
            const offPeakInput = document.getElementById('offPeakRate');
            const superOffPeakInput = document.getElementById('superOffPeakRate');
            const baselineCreditInput = document.getElementById('baselineCredit');
            const solarDiscountInput = document.getElementById('solarDiscount');

            return {
                midPeakRate: midPeakInput ? parseFloat(midPeakInput.value) : undefined,
                onPeak: onPeakInput ? parseFloat(onPeakInput.value) : undefined,
                offPeak: parseFloat(offPeakInput?.value || 0),
                superOffPeak: superOffPeakInput ? parseFloat(superOffPeakInput.value) : undefined,
                baselineCredit: parseFloat(baselineCreditInput?.value || 0),
                solarDiscount: parseFloat(solarDiscountInput?.value || 0)
            };
        }

        // Get current usage from inputs
        function getCurrentUsage() {
            const onPeakUsageEl = document.getElementById('onPeakUsage');
            const offPeakUsageEl = document.getElementById('offPeakUsage');
            const baselineCreditUsageEl = document.getElementById('baselineCreditUsage');
            
            const usage = {
                onPeak: parseFloat(onPeakUsageEl?.value || 0),
                offPeak: parseFloat(offPeakUsageEl?.value || 0),
                baselineCredit: parseFloat(baselineCreditUsageEl?.value || 0),
                superOffPeak: 0 // Default to 0, can be modified for three-tier rates
            };
            
            // For three-tier rates, map on-peak to mid-peak
            if (currentRates.midPeakRate !== undefined) {
                usage.midPeak = usage.onPeak;
                usage.onPeak = 0; // Set to 0 for three-tier rates
            }
            
            return usage;
        }

        // Calculate solar savings
        function calculateSolarSavings() {
            const rates = getCurrentRates();
            const usage = getCurrentUsage();
            const isThreeTier = rates.midPeakRate !== undefined;

            let energyCosts = {};
            let totalEnergyCost = 0;

            if (isThreeTier) {
                energyCosts.midPeakCost = usage.midPeak * rates.midPeakRate;
                energyCosts.offPeakCost = usage.offPeak * rates.offPeak;
                energyCosts.superOffPeakCost = usage.superOffPeak * (rates.superOffPeak || 0);
                totalEnergyCost = energyCosts.midPeakCost + energyCosts.offPeakCost + energyCosts.superOffPeakCost;
            } else {
                energyCosts.onPeakCost = usage.onPeak * rates.onPeak;
                energyCosts.offPeakCost = usage.offPeak * rates.offPeak;
                totalEnergyCost = energyCosts.onPeakCost + energyCosts.offPeakCost;
            }

            const baselineCreditAmount = usage.baselineCredit * rates.baselineCredit;
            const subtotal = totalEnergyCost - baselineCreditAmount;
            
            let careDiscountAmount = 0;
            let afterCareDiscount = subtotal;
            
            // Apply CARE discount if customer is on CARE program
            if (isCareCustomer) {
                const careDiscountRate = CARE_DISCOUNTS[currentRates.utility] || 0;
                careDiscountAmount = subtotal * careDiscountRate;
                afterCareDiscount = subtotal - careDiscountAmount;
            }
            
            const solarDiscountAmount = afterCareDiscount * (rates.solarDiscount / 100);
            const finalAmount = afterCareDiscount - solarDiscountAmount;
            
            const totalKwh = usage.onPeak + usage.offPeak + usage.superOffPeak + usage.midPeak;
            const avgRatePerKwh = totalKwh > 0 ? finalAmount / totalKwh : 0;
            const co2Saved = totalKwh * 0.284; // kg CO2 per kWh
            const milesEquivalent = co2Saved * 2.5; // miles of driving equivalent

            calculations = {
                ...energyCosts,
                baselineCreditAmount: baselineCreditAmount,
                subtotal: subtotal,
                careDiscountAmount: careDiscountAmount,
                afterCareDiscount: afterCareDiscount,
                solarDiscountAmount: solarDiscountAmount,
                finalAmount: finalAmount,
                totalKwh: totalKwh,
                avgRatePerKwh: avgRatePerKwh,
                co2Saved: co2Saved,
                milesEquivalent: milesEquivalent,
                isThreeTier: isThreeTier,
                isCareCustomer: isCareCustomer
            };

            displayResults();
        }

        // Display calculation results
        function displayResults() {
            const isThreeTier = calculations.isThreeTier;
            const isCare = calculations.isCareCustomer;
            
            // Update results title
            document.getElementById('resultsTitle').textContent = 
                `Solar Energy Calculation Results ${isCare ? '(CARE Customer)' : ''}`;
            
            const costBreakdown = isThreeTier ? `
                <div class="result-item">
                    <span>Mid-Peak Cost:</span>
                    <span class="result-value">${calculations.midPeakCost?.toFixed(2) || '0.00'}</span>
                </div>
                <div class="result-item">
                    <span>Off-Peak Cost:</span>
                    <span class="result-value">${calculations.offPeakCost?.toFixed(2) || '0.00'}</span>
                </div>
                <div class="result-item">
                    <span>Super Off-Peak Cost:</span>
                    <span class="result-value">${calculations.superOffPeakCost?.toFixed(2) || '0.00'}</span>
                </div>
            ` : `
                <div class="result-item">
                    <span>On-Peak Cost:</span>
                    <span class="result-value">${calculations.onPeakCost?.toFixed(2) || '0.00'}</span>
                </div>
                <div class="result-item">
                    <span>Off-Peak Cost:</span>
                    <span class="result-value">${calculations.offPeakCost?.toFixed(2) || '0.00'}</span>
                </div>
            `;

            const careSection = isCare ? `
                <div class="result-item">
                    <span>CARE Discount:</span>
                    <span class="result-value positive">-${calculations.careDiscountAmount?.toFixed(2) || '0.00'}</span>
                </div>
                <div class="result-item">
                    <span>After CARE Discount:</span>
                    <span class="result-value">${calculations.afterCareDiscount?.toFixed(2) || '0.00'}</span>
                </div>
            ` : '';

            document.getElementById('resultsContent').innerHTML = `
                <div class="results-grid">
                    <div>
                        ${costBreakdown}
                        <div class="result-item">
                            <span>Baseline Credit:</span>
                            <span class="result-value positive">-${calculations.baselineCreditAmount?.toFixed(2) || '0.00'}</span>
                        </div>
                        <div class="result-item total">
                            <span>Subtotal:</span>
                            <span class="result-value">${calculations.subtotal?.toFixed(2) || '0.00'}</span>
                        </div>
                    </div>
                    
                    <div>
                        ${careSection}
                        <div class="result-item">
                            <span>Solar Discount:</span>
                            <span class="result-value positive">-${calculations.solarDiscountAmount?.toFixed(2) || '0.00'}</span>
                        </div>
                        <div class="result-item total">
                            <span><strong>Final Amount:</strong></span>
                            <span class="result-value large">${calculations.finalAmount?.toFixed(2) || '0.00'}</span>
                        </div>
                        <div class="result-item">
                            <span>Total kWh:</span>
                            <span class="result-value">${calculations.totalKwh?.toFixed(3) || '0.000'}</span>
                        </div>
                        <div class="result-item">
                            <span>Avg Rate/kWh:</span>
                            <span class="result-value">${calculations.avgRatePerKwh?.toFixed(4) || '0.0000'}</span>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('environmentalResults').innerHTML = `
                <div class="env-card green">
                    <div class="env-value green">${calculations.co2Saved?.toFixed(1) || '0.0'} kg</div>
                    <div class="env-label green">CO₂ Emissions Saved</div>
                </div>
                <div class="env-card orange">
                    <div class="env-value orange">${calculations.milesEquivalent?.toFixed(0) || '0'}</div>
                    <div class="env-label orange">Miles of Driving Equivalent</div>
                </div>
            `;

            // Show results section with animation
            document.getElementById('resultsSection').classList.add('show');
            
            // Scroll to results
            document.getElementById('resultsSection').scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }

        // Initialize the application when the page loads
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
