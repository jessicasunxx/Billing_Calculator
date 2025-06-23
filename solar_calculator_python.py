#!/usr/bin/env python3
"""
Solar Energy Calculator
Converts the TSX React component to Python for backend processing
Data extracted from PX_Feb_CommunityA 1.xlsx and Rate Breakdown 2.xlsx
"""

import pandas as pd
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class UsageData:
    """Energy usage data structure"""
    on_peak: float = 0.0
    off_peak: float = 0.0
    mid_peak: float = 0.0
    super_off_peak: float = 0.0
    baseline_credit: float = 0.0


@dataclass
class RateStructure:
    """Utility rate structure"""
    name: str
    utility: str
    effective_date: str
    time_structure: Dict[str, str]
    rates: Dict[str, Dict[str, float]]
    baseline_allocation: Optional[Dict] = None
    minimum_delivery_charge: float = 0.0
    care_discount: float = 0.0
    solar_discount: float = 0.075


@dataclass
class CalculationResult:
    """Solar savings calculation result"""
    usage: UsageData
    rate_structure: str
    season: str
    is_care: bool
    energy_cost: float
    baseline_credit_amount: float
    subtotal: float
    care_discount_amount: float = 0.0
    solar_discount_amount: float = 0.0
    final_amount: float = 0.0
    total_kwh: float = 0.0
    avg_rate_per_kwh: float = 0.0
    co2_saved: float = 0.0
    miles_equivalent: float = 0.0


class SolarCalculator:
    """Main solar energy calculator class"""
    
    def __init__(self):
        self.utility_rates = self._load_utility_rates()
        self.customer_accounts = self._load_customer_accounts()
        
    def _load_utility_rates(self) -> Dict:
        """Load utility rates from Excel data"""
        return {
            'PGE_RATES': {
                'E-TOU-C-NEM2': RateStructure(
                    name='E-TOU-C-NEM2 Residential - Time of Use - Rate C (NEM 2.0)',
                    utility='PG&E',
                    effective_date='2025-03-01',
                    time_structure={
                        'on_peak': 'Weekdays 4pm - 9pm',
                        'off_peak': 'Weekdays 9pm - 4pm, All Weekends, Holidays'
                    },
                    rates={
                        'winter': {
                            'on_peak': 0.50085,
                            'off_peak': 0.47085,
                            'baseline_credit': 0.10301
                        },
                        'summer': {
                            'on_peak': 0.52085,
                            'off_peak': 0.49085,
                            'baseline_credit': 0.10301
                        }
                    },
                    baseline_allocation={
                        'territory_X': {'basic_electric': 9.7, 'all_electric': 14.6},
                        'territory_T': {'basic_electric': 7.5, 'all_electric': 12.9}
                    },
                    minimum_delivery_charge=0.39167,
                    care_discount=0.34964,
                    solar_discount=0.075
                ),
                'E-TOU-D-NEM2': RateStructure(
                    name='E-TOU-D-NEM2 Residential - Time of Use - Rate D (NEM 2.0)',
                    utility='PG&E',
                    effective_date='2025-03-01',
                    time_structure={
                        'on_peak': 'Weekdays 5pm - 8pm',
                        'off_peak': 'Weekdays 8pm - 5pm, All Weekends, Holidays'
                    },
                    rates={
                        'winter': {
                            'on_peak': 0.48189,
                            'off_peak': 0.44328,
                            'baseline_credit': 0.10301
                        },
                        'summer': {
                            'on_peak': 0.50189,
                            'off_peak': 0.46328,
                            'baseline_credit': 0.10301
                        }
                    },
                    baseline_allocation={'territory_X': 9.7, 'territory_T': 7.5},
                    minimum_delivery_charge=0.40317,
                    care_discount=0.34964,
                    solar_discount=0.075
                )
            },
            'SCE_RATES': {
                'TOU-D-4-9PM-NEM2': RateStructure(
                    name='TOU-D-4-9PM-NEM2 Time-Of-Use Residential',
                    utility='SCE',
                    effective_date='2025-03-01',
                    time_structure={
                        'mid_peak': 'Weekdays 4pm - 9pm',
                        'off_peak': 'Weekdays 9pm - 8am, All Weekends',
                        'super_off_peak': 'Weekdays 8am - 4pm'
                    },
                    rates={
                        'winter': {
                            'mid_peak': 0.48241,
                            'off_peak': 0.32487,
                            'super_off_peak': 0.28820,
                            'baseline_credit': 0.09444
                        },
                        'summer': {
                            'mid_peak': 0.52241,
                            'off_peak': 0.34487,
                            'super_off_peak': 0.30820,
                            'baseline_credit': 0.09444
                        }
                    },
                    care_discount=0.325,
                    solar_discount=0.075
                )
            }
        }
    
    def _load_customer_accounts(self) -> Dict:
        """Load customer account data"""
        return {
            'Community A': {
                'accounts': [
                    {
                        'subscriber_id': 700232948440589,
                        'account_id': 180,
                        'tariff_code': 'E-TOU-C-NEM2',
                        'tariff_name': 'Residential - Time of Use - Rate C (NEM 2.0)',
                        'rate_criteria': 'None',
                        'billing_periods': [
                            {'start': '2025-01-01', 'end': '2025-02-01'},
                            {'start': '2025-02-01', 'end': '2025-03-01'},
                            {'start': '2025-03-01', 'end': '2025-04-01'}
                        ]
                    },
                    {
                        'subscriber_id': 700232943199617,
                        'account_id': 432,
                        'tariff_code': 'EL-TOU-C-NEM2',
                        'tariff_name': 'Residential - Time of Use - CARE (NEM 2.0)',
                        'rate_criteria': 'CARE',
                        'billing_periods': [
                            {'start': '2025-01-01', 'end': '2025-02-01'},
                            {'start': '2025-02-01', 'end': '2025-03-01'},
                            {'start': '2025-03-01', 'end': '2025-04-01'}
                        ]
                    }
                ]
            }
        }
    
    def get_rate_structure(self, utility: str, tariff_code: str) -> Optional[RateStructure]:
        """Get rate structure by utility and tariff code"""
        if utility == 'PG&E' and tariff_code in self.utility_rates['PGE_RATES']:
            return self.utility_rates['PGE_RATES'][tariff_code]
        elif utility == 'SCE' and tariff_code in self.utility_rates['SCE_RATES']:
            return self.utility_rates['SCE_RATES'][tariff_code]
        return None
    
    def calculate_bill(self, usage: UsageData, rate_structure: RateStructure, 
                      season: str = 'winter', is_care: bool = False) -> CalculationResult:
        """Calculate solar energy bill"""
        rates = rate_structure.rates[season]
        
        # Initialize result
        result = CalculationResult(
            usage=usage,
            rate_structure=rate_structure.name,
            season=season,
            is_care=is_care,
            energy_cost=0.0,
            baseline_credit_amount=0.0,
            subtotal=0.0
        )
        
        # Calculate energy costs by tier
        if 'mid_peak' in rates:
            # Three-tier rate structure (SCE)
            mid_peak_cost = usage.mid_peak * rates['mid_peak']
            off_peak_cost = usage.off_peak * rates['off_peak']
            super_off_peak_cost = usage.super_off_peak * rates['super_off_peak']
            result.energy_cost = mid_peak_cost + off_peak_cost + super_off_peak_cost
        else:
            # Two-tier rate structure (PG&E)
            on_peak_cost = usage.on_peak * rates['on_peak']
            off_peak_cost = usage.off_peak * rates['off_peak']
            result.energy_cost = on_peak_cost + off_peak_cost
        
        # Apply baseline credit
        result.baseline_credit_amount = usage.baseline_credit * rates['baseline_credit']
        result.subtotal = result.energy_cost - result.baseline_credit_amount
        
        # Apply CARE discount if applicable
        if is_care:
            result.care_discount_amount = result.subtotal * rate_structure.care_discount
            after_care = result.subtotal - result.care_discount_amount
        else:
            after_care = result.subtotal
        
        # Apply solar discount
        result.solar_discount_amount = result.subtotal * rate_structure.solar_discount
        result.final_amount = result.subtotal - result.solar_discount_amount
        
        # Calculate totals and environmental impact
        result.total_kwh = usage.on_peak + usage.off_peak + usage.mid_peak + usage.super_off_peak
        result.avg_rate_per_kwh = result.subtotal / result.total_kwh if result.total_kwh > 0 else 0
        result.co2_saved = result.total_kwh * 0.284  # kg CO2 per kWh
        result.miles_equivalent = result.co2_saved * 2.5  # miles of driving equivalent
        
        return result
    
    def process_csv_data(self, csv_file_path: str) -> List[CalculationResult]:
        """Process CSV file and calculate solar savings for each row"""
        try:
            df = pd.read_csv(csv_file_path)
            results = []
            
            for _, row in df.iterrows():
                usage = self._format_usage_from_csv(row)
                
                # Assume PG&E E-TOU-D-NEM2 if not specified
                utility = row.get('utility', 'PG&E')
                tariff_code = row.get('tariff_code', 'E-TOU-D-NEM2')
                season = row.get('season', 'winter')
                is_care = row.get('is_care', False)
                
                rate_structure = self.get_rate_structure(utility, tariff_code)
                if rate_structure:
                    result = self.calculate_bill(usage, rate_structure, season, is_care)
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error processing CSV file: {e}")
            return []
    
    def _format_usage_from_csv(self, row: pd.Series) -> UsageData:
        """Format usage data from CSV row"""
        return UsageData(
            on_peak=float(row.get('on_peak_usage', row.get('onPeakUsage', 0))),
            off_peak=float(row.get('off_peak_usage', row.get('offPeakUsage', 0))),
            mid_peak=float(row.get('mid_peak_usage', row.get('midPeakUsage', 0))),
            super_off_peak=float(row.get('super_off_peak_usage', row.get('superOffPeakUsage', 0))),
            baseline_credit=float(row.get('baseline_credit', row.get('baselineCredit', 0)))
        )
    
    def export_results_to_csv(self, results: List[CalculationResult], output_path: str):
        """Export calculation results to CSV"""
        data = []
        for result in results:
            row = {
                'rate_structure': result.rate_structure,
                'season': result.season,
                'is_care': result.is_care,
                'on_peak_usage': result.usage.on_peak,
                'off_peak_usage': result.usage.off_peak,
                'mid_peak_usage': result.usage.mid_peak,
                'super_off_peak_usage': result.usage.super_off_peak,
                'baseline_credit_usage': result.usage.baseline_credit,
                'energy_cost': result.energy_cost,
                'baseline_credit_amount': result.baseline_credit_amount,
                'subtotal': result.subtotal,
                'care_discount_amount': result.care_discount_amount,
                'solar_discount_amount': result.solar_discount_amount,
                'final_amount': result.final_amount,
                'total_kwh': result.total_kwh,
                'avg_rate_per_kwh': result.avg_rate_per_kwh,
                'co2_saved_kg': result.co2_saved,
                'miles_equivalent': result.miles_equivalent
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"Results exported to {output_path}")
    
    def print_calculation_summary(self, result: CalculationResult):
        """Print a formatted summary of the calculation"""
        print(f"\n=== Solar Energy Calculation Results ===")
        print(f"Rate Structure: {result.rate_structure}")
        print(f"Season: {result.season.capitalize()}")
        print(f"CARE Customer: {'Yes' if result.is_care else 'No'}")
        print(f"\nUsage:")
        print(f"  On-Peak: {result.usage.on_peak:.3f} kWh")
        print(f"  Off-Peak: {result.usage.off_peak:.3f} kWh")
        if result.usage.mid_peak > 0:
            print(f"  Mid-Peak: {result.usage.mid_peak:.3f} kWh")
        if result.usage.super_off_peak > 0:
            print(f"  Super Off-Peak: {result.usage.super_off_peak:.3f} kWh")
        print(f"  Baseline Credit: {result.usage.baseline_credit:.3f} kWh")
        print(f"\nCosts:")
        print(f"  Energy Cost: ${result.energy_cost:.2f}")
        print(f"  Baseline Credit: -${result.baseline_credit_amount:.2f}")
        print(f"  Subtotal: ${result.subtotal:.2f}")
        if result.care_discount_amount > 0:
            print(f"  CARE Discount: -${result.care_discount_amount:.2f}")
        print(f"  Solar Discount: -${result.solar_discount_amount:.2f}")
        print(f"  Final Amount: ${result.final_amount:.2f}")
        print(f"\nSummary:")
        print(f"  Total kWh: {result.total_kwh:.3f}")
        print(f"  Average Rate: ${result.avg_rate_per_kwh:.4f}/kWh")
        print(f"\nEnvironmental Impact:")
        print(f"  CO₂ Saved: {result.co2_saved:.1f} kg")
        print(f"  Driving Equivalent: {result.miles_equivalent:.0f} miles")


def main():
    """Example usage of the Solar Calculator"""
    calculator = SolarCalculator()
    
    # Example usage data (from your original TSX component)
    usage = UsageData(
        on_peak=6.333,
        off_peak=126.074,
        baseline_credit=132.407
    )
    
    # Get PG&E E-TOU-D-NEM2 rate structure
    rate_structure = calculator.get_rate_structure('PG&E', 'E-TOU-D-NEM2')
    
    if rate_structure:
        # Calculate for regular customer
        result = calculator.calculate_bill(usage, rate_structure, 'winter', False)
        calculator.print_calculation_summary(result)
        
        # Calculate for CARE customer
        care_result = calculator.calculate_bill(usage, rate_structure, 'winter', True)
        print(f"\n--- CARE Customer Comparison ---")
        print(f"Regular Customer Final Amount: ${result.final_amount:.2f}")
        print(f"CARE Customer Final Amount: ${care_result.final_amount:.2f}")
        print(f"CARE Savings: ${result.final_amount - care_result.final_amount:.2f}")
    
    # Example of processing CSV data
    # results = calculator.process_csv_data('usage_data.csv')
    # calculator.export_results_to_csv(results, 'solar_calculations_output.csv')


if __name__ == "__main__":
    main()