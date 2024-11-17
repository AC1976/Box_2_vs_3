import pandas as pd

class Box3:
    def __init__(self, initial_equity: float, initial_bonds: float, initial_property: float, 
                 market_return_rate: float, dividend_yield: float, coupon: float, rental_return: float, inflation: float, 
                 partners: bool):
        self.results = []
        self.initial_equity = initial_equity
        self.initial_bonds = initial_bonds
        self.initial_property = initial_property
        self.column_names = [
            'equity_start',         # Column 0
            'bonds_start',          # Column 1
            'property_start',       # Column 2
            'equity_return',        # Column 3
            'dividend_yield',       # Column 4
            'bond_coupon',          # Column 5
            'net_rent',             # Column 6
            'tax_income',           # Column 7
            'current_tax',          # Column 8
            'cash_account',         # Column 9
            'equity_fv',            # Column 10
            'bonds_fv',             # Column 11
            'property_fv',          # Column 12
            'equity_bv',            # Column 13
            'bonds_bv',             # Column 14
            'property_bv',          # Column 15
            'gain',                 # Column 16
            'deferred_tax',         # Column 17
            'investment_value',     # Column 18
            'exit_tax',             # Column 19
            'net_value',            # Column 20
            ]
        
        self.market_return_rate=market_return_rate
        self.dividend_yield=dividend_yield
        self.coupon=coupon
        self.rental_return=rental_return 
        self.inflation=inflation
        self.partners=partners
    
    def get_previous_year_value(self, year: int, column_index: int, default_value: float = 0.0) -> float:
        """
        Get value from previous year for a specific column.
        Returns default_value if it's the first year or column doesn't exist.
        """
        if year == 0:
            return default_value
        return self.results[year - 1][column_index]
    
    def calculate_year(self, year, franchise=1250,
                        box3Rate=0.36):
        
        """Calculate all values for a given year, with references to previous year's data."""
        
        # Initialize row
        row = [0] * len(self.column_names)
        
        # Columns 0, 1, 2: Start values 
        row[0] = self.initial_equity if year == 0 else self.get_previous_year_value(year,10)  # 10 is equity_fv
        row[1] = self.initial_bonds if year == 0 else self.get_previous_year_value(year, 11)  # 11 is bonds_fv
        row[2] = self.initial_property if year == 0 else self.get_previous_year_value(year, 12)  # 12 is property_fv
        
        # Columns 3, 4, 5, 6: Market return calculations
        row[3] = row[0] * self.market_return_rate
        row[4] = row[0] * self.dividend_yield
        row[5] = row[1] * self.coupon
        row[6] = row[2] * self.rental_return
    
        # Column 7, 8: taxable income and current tax expense
        row[7] = row[3]+row[4]+row[5]+row[6]
        row[8] = (row[7]-2*franchise)*box3Rate if self.partners is True else (row[7]-franchise)*box3Rate
                                                                       
        # Column 9: cash account
        prior_cash_balance = 0 if year == 0 else self.get_previous_year_value(year, 9)  # 9 is cash_account
        row[9] = row[4]+row[5]+row[6]-row[8] + prior_cash_balance
        
        # Column 10, 11, 12: Fair value of investments
        row[10] = row[0] + row [3]
        row[11] = row[1]
        row[12] = row[2] * (1+self.inflation)

        # Column 13, 14, 15: Book value of investments
        row[13] = row[10]
        row[14] = self.initial_bonds
        row[15] = self.initial_property
        
        # Column 16, 17: Deferred gain and tax
        row[16] = (row[10]+row[11]+row[12]) - (row[13]+row[14]+row[15]) ## Fair value minus cost price = gain
        row[17] = row[16] * box3Rate

        # Column 18, 19, 20: Box 2 values and tax
        row[18] = row[9]+row[10]+row[11]+row[12]
        row[19] = row[17]
        row[20] = row[18] - row[19]
                
        self.results.append(row)
        return row
    
    def run_model(self, years):
        """Run the model for specified number of years."""
        for year in range(years):
            self.calculate_year(year)
        
        results = self.results
        df = pd.DataFrame(results, columns=self.column_names).astype('int')
        return df

    def chart_data(self, years):
        data = self.run_model(years)
        df = data[['investment_value', 'exit_tax', 'net_value']]
        return df

'''
bram_spaarpot = Box3(initial_equity=10000, initial_bonds=10000, initial_property=0,
                market_return_rate=0.06,
                dividend_yield=0.02,
                coupon=0.035,
                rental_return=0.065,
                
                inflation=0.02,
                partners=True,
                )

print(bram_spaarpot.chart_data(50))

'''