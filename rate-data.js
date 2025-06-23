// rate-data.js
// Extracted rate data from PG&E and SCE Excel files

const UTILITY_RATES = {
  // PG&E Rates extracted from "Rate Breakdown 2.xlsx"
  PGE_RATES: {
    'E-TOU-C-NEM2': {
      name: 'E-TOU-C-NEM2 Residential - Time of Use - Rate C (NEM 2.0)',
      utility: 'PG&E',
      effectiveDate: '2025-03-01',
      timeStructure: {
        onPeak: 'Weekdays 4pm - 9pm',
        offPeak: 'Weekdays 9pm - 4pm, All Weekends, Holidays'
      },
      rates: {
        winter: {
          onPeak: 0.50085,      // Total rate from Excel
          offPeak: 0.47085,     // Total rate from Excel
          baselineCredit: 0.10301
        },
        summer: {
          onPeak: 0.52085,      // Estimated summer rates (typically higher)
          offPeak: 0.49085,
          baselineCredit: 0.10301
        }
      },
      baselineAllocation: {
        territory_X: {
          basicElectric: 9.7,
          allElectric: 14.6
        },
        territory_T: {
          basicElectric: 7.5,
          allElectric: 12.9
        }
      },
      minimumDeliveryCharge: 0.39167,
      careDiscount: 0.34964,  // From CARE Details sheet
      solarDiscount: 0.075
    },
    
    'E-TOU-D-NEM2': {
      name: 'E-TOU-D-NEM2 Residential - Time of Use - Rate D (NEM 2.0)',
      utility: 'PG&E',
      effectiveDate: '2025-03-01',
      timeStructure: {
        onPeak: 'Weekdays 5pm - 8pm',
        offPeak: 'Weekdays 8pm - 5pm, All Weekends, Holidays'
      },
      rates: {
        winter: {
          onPeak: 0.48189,      // Total rate from Excel
          offPeak: 0.44328,     // Total rate from Excel
          baselineCredit: 0.10301
        },
        summer: {
          onPeak: 0.50189,      // Estimated summer rates
          offPeak: 0.46328,
          baselineCredit: 0.10301
        }
      },
      baselineAllocation: {
        territory_X: 9.7,
        territory_T: 7.5
      },
      minimumDeliveryCharge: 0.40317,
      careDiscount: 0.34964,
      solarDiscount: 0.075
    }
  },

  // SCE Rates (estimated based on typical structures)
  SCE_RATES: {
    'TOU-D-4-9PM-NEM2': {
      name: 'TOU-D-4-9PM-NEM2 Time-Of-Use Residential',
      utility: 'SCE',
      effectiveDate: '2025-03-01',
      timeStructure: {
        midPeak: 'Weekdays 4pm - 9pm',
        offPeak: 'Weekdays 9pm - 8am, All Weekends',
        superOffPeak: 'Weekdays 8am - 4pm'
      },
      rates: {
        winter: {
          midPeakRate: 0.48241,
          offPeakRate: 0.32487,
          superOffPeakRate: 0.28820,
          baselineCredit: 0.09444
        },
        summer: {
          midPeakRate: 0.52241,
          offPeakRate: 0.34487,
          superOffPeakRate: 0.30820,
          baselineCredit: 0.09444
        }
      },
      careDiscount: 0.325,    // SCE CARE discount from Excel
      solarDiscount: 0.075
    },
    
    'TOU-D-5-8PM-NEM2': {
      name: 'TOU-D-5-8PM-NEM2 Time-Of-Use Residential',
      utility: 'SCE',
      effectiveDate: '2025-03-01',
      timeStructure: {
        onPeak: 'Weekdays 5pm - 8pm',
        offPeak: 'All other hours'
      },
      rates: {
        winter: {
          onPeak: 0.46000,
          offPeak: 0.31000,
          baselineCredit: 0.09444
        },
        summer: {
          onPeak: 0.50000,
          offPeak: 0.33000,
          baselineCredit: 0.09444
        }
      },
      careDiscount: 0.325,
      solarDiscount: 0.075
    }
  }
};

// Customer account data structure (based on "PX_Feb_CommunityA 1.xlsx")
const CUSTOMER_ACCOUNTS = {
  'Community A': {
    accounts: [
      {
        subscriberId: 700232948440589,
        accountId: 180,
        tariffCode: 'E-TOU-C-NEM2',
        tariffName: 'Residential - Time of Use - Rate C (NEM 2.0)',
        rateCriteria: 'None',
        billingPeriods: [
          { start: '2025-01-01', end: '2025-02-01' },
          { start: '2025-02-01', end: '2025-03-01' },
          { start: '2025-03-01', end: '2025-04-01' }
        ]
      },
      {
        subscriberId: 700232943199617,
        accountId: 432,
        tariffCode: 'EL-TOU-C-NEM2',
        tariffName: 'Residential - Time of Use - CARE (NEM 2.0)',
        rateCriteria: 'CARE',
        billingPeriods: [
          { start: '2025-01-01', end: '2025-02-01' },
          { start: '2025-02-01', end: '2025-03-01' },
          { start: '2025-03-01', end: '2025-04-01' }
        ]
      },
      {
        subscriberId: 954315962804160,
        accountId: 50893,
        tariffCode: 'EL-TOU-C-EH-NEM2',
        tariffName: 'EL-TOU-C-EH-NEM2 Residential - Time of Use - CARE - Electric Heat',
        rateCriteria: 'CARE',
        billingPeriods: [
          { start: '2025-01-01', end: '2025-02-01' },
          { start: '2025-02-01', end: '2025-03-01' },
          { start: '2025-03-01', end: '2025-04-01' }
        ]
      },
      {
        subscriberId: 371003287380944,
        accountId: 50966,
        tariffCode: 'E-TOU-C-EH-NEM2',
        tariffName: 'E-TOU-C-EH-NEM2 Residential - Time of Use - Electric Heat (NEM 2.0)',
        rateCriteria: 'None',
        billingPeriods: [
          { start: '2025-01-01', end: '2025-02-01' },
          { start: '2025-02-01', end: '2025-03-01' },
          { start: '2025-03-01', end: '2025-04-01' }
        ]
      },
      {
        subscriberId: 700232944861926,
        accountId: 61023,
        tariffCode: 'E-TOU-D-NEM2 Residential',
        tariffName: 'E-TOU-D-NEM2 Residential - Time of Use - Rate D (NEM 2.0)',
        rateCriteria: 'None',
        billingPeriods: [
          { start: '2025-01-18', end: '2025-02-01' },
          { start: '2025-02-01', end: '2025-03-01' },
          { start: '2025-03-01', end: '2025-04-01' }
        ]
      }
    ]
  }
};

// CARE program details (from CARE Details sheet)
const CARE_PROGRAM = {
  pgeDiscount: 0.34964,        // 34.964% discount on eligible charges
  sceDiscount: 0.325,          // 32.5% discount on eligible charges
  deliveryMinimumDiscount: 0.5, // 50% discount on delivery minimum
  pgeCarePortionPPP: 0.01281   // PG&E CARE portion of Public Purpose Programs
};

// Rate calculation utilities
const RateCalculator = {
  /**
   * Calculate bill amount for given usage and rate structure
   * @param {Object} usage - Usage data { onPeak, offPeak, midPeak, superOffPeak, baselineCredit }
   * @param {Object} rateStructure - Rate structure object
   * @param {string} season - 'winter' or 'summer'
   * @param {boolean} isCare - Whether customer is on CARE program
   * @returns {Object} Calculation breakdown
   */
  calculateBill(usage, rateStructure, season = 'winter', isCare = false) {
    const rates = rateStructure.rates[season];
    let calculation = {
      usage: usage,
      rateStructure: rateStructure.name,
      season: season,
      isCare: isCare
    };

    // Calculate costs by tier
    if (rates.midPeakRate !== undefined) {
      // Three-tier rate structure (SCE)
      calculation.midPeakCost = (usage.midPeak || 0) * rates.midPeakRate;
      calculation.offPeakCost = (usage.offPeak || 0) * rates.offPeakRate;
      calculation.superOffPeakCost = (usage.superOffPeak || 0) * rates.superOffPeakRate;
      calculation.energyCost = calculation.midPeakCost + calculation.offPeakCost + calculation.superOffPeakCost;
    } else {
      // Two-tier rate structure (PG&E)
      calculation.onPeakCost = (usage.onPeak || 0) * rates.onPeak;
      calculation.offPeakCost = (usage.offPeak || 0) * rates.offPeak;
      calculation.energyCost = calculation.onPeakCost + calculation.offPeakCost;
    }

    // Apply baseline credit
    calculation.baselineCreditAmount = (usage.baselineCredit || 0) * rates.baselineCredit;
    calculation.subtotal = calculation.energyCost - calculation.baselineCreditAmount;

    // Apply CARE discount if applicable
    if (isCare) {
      const careDiscount = rateStructure.utility === 'PG&E' ? CARE_PROGRAM.pgeDiscount : CARE_PROGRAM.sceDiscount;
      calculation.careDiscountAmount = calculation.subtotal * careDiscount;
      calculation.afterCareDiscount = calculation.subtotal - calculation.careDiscountAmount;
    }

    // Apply solar discount
    const solarDiscountAmount = calculation.subtotal * (rateStructure.solarDiscount || 0);
    calculation.solarDiscountAmount = solarDiscountAmount;
    calculation.finalAmount = calculation.subtotal - solarDiscountAmount;

    // Calculate totals and averages
    calculation.totalKwh = (usage.onPeak || 0) + (usage.offPeak || 0) + (usage.midPeak || 0) + (usage.superOffPeak || 0);
    calculation.avgRatePerKwh = calculation.totalKwh > 0 ? calculation.subtotal / calculation.totalKwh : 0;

    // Environmental impact
    calculation.co2Saved = calculation.totalKwh * 0.284; // kg CO2 per kWh
    calculation.milesEquivalent = calculation.co2Saved * 2.5; // miles of driving equivalent

    return calculation;
  },

  /**
   * Get rate structure by utility and tariff code
   * @param {string} utility - 'PG&E' or 'SCE'
   * @param {string} tariffCode - Tariff code
   * @returns {Object|null} Rate structure object
   */
  getRateStructure(utility, tariffCode) {
    if (utility === 'PG&E' && UTILITY_RATES.PGE_RATES[tariffCode]) {
      return UTILITY_RATES.PGE_RATES[tariffCode];
    } else if (utility === 'SCE' && UTILITY_RATES.SCE_RATES[tariffCode]) {
      return UTILITY_RATES.SCE_RATES[tariffCode];
    }
    return null;
  },

  /**
   * Convert usage data from CSV format to calculator format
   * @param {Object} csvRow - Row from CSV data
   * @returns {Object} Formatted usage data
   */
  formatUsageFromCSV(csvRow) {
    return {
      onPeak: parseFloat(csvRow['On Peak Usage'] || csvRow['onPeakUsage'] || 0),
      offPeak: parseFloat(csvRow['Off Peak Usage'] || csvRow['offPeakUsage'] || 0),
      midPeak: parseFloat(csvRow['Mid Peak Usage'] || csvRow['midPeakUsage'] || 0),
      superOffPeak: parseFloat(csvRow['Super Off Peak Usage'] || csvRow['superOffPeakUsage'] || 0),
      baselineCredit: parseFloat(csvRow['Baseline Credit'] || csvRow['baselineCredit'] || 0)
    };
  }
};

// Default usage examples for testing
const SAMPLE_USAGE_DATA = {
  residential_typical: {
    onPeak: 6.333,
    offPeak: 126.074,
    baselineCredit: 132.407
  },
  residential_high: {
    onPeak: 15.5,
    offPeak: 285.2,
    baselineCredit: 200.0
  },
  residential_low: {
    onPeak: 2.1,
    offPeak: 45.8,
    baselineCredit: 47.9
  },
  three_tier_example: {
    midPeak: 8.5,
    offPeak: 95.3,
    superOffPeak: 22.1,
    baselineCredit: 125.9
  }
};

// Export for use in other modules (if using ES6 modules)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    UTILITY_RATES,
    CUSTOMER_ACCOUNTS,
    CARE_PROGRAM,
    RateCalculator,
    SAMPLE_USAGE_DATA
  };
}