import numpy as np
import pandas as pd

## configuration parameters used by models


config = {'equity' : 1000000,
        'bonds' : 1000000,
        'property' : 1000000,
        'equity_return' : 0.062,
        'bonds_return' : 0.035,
        'property_return' : 0.06,
        'inflation' : 0.02,
        'box2Rate_slice1' : 0.245,
        'box2Rate_slice2' : 0.31,
        'box2_slices_at' : 67000,
        'box3Rate' : 0.36,
        'box3_freezone' : 2500,
        'vpbRate_slice1' : 0.19,
        'vpbRate_slice2' : 0.258,
        'vpb_slices_at' : 200000,
        'bv_fees' : 3000,
        'term' : 50
        }


class boxer:

    def __init__(self, **parameters):
        
        for k, v in parameters.items():
            setattr(self, k, v)
                    
    def _box2_calc(self):
        
        matrix = np.zeros((self.term, 20), dtype=int)

        '''initialize first row of matrix'''
        
        ## INVESTMENTS & RETURNS
        matrix[0][0] = self.equity                                                         # equity
        matrix[0][1] = self.bonds                                                          # bonds
        matrix[0][2] = self.property                                                       # property
        matrix[0][3] = matrix[0][0] * self.equity_return                                   # return on equity
        matrix[0][4] = matrix[0][1] * self.bonds_return                                    # return on bonds
        matrix[0][5] = matrix[0][2] * self.property_return                                 # return on property (net rent)
        
        ## VPB CURRENT AND AFTER TAX CASH
        matrix[0][6] = matrix[0][4] + matrix[0][5] - self.bv_fees                       # jaarwinst
                                                                                        # Vpb current
        if matrix[0][6] > self.vpb_slices_at:                                               
            matrix[0][7] = (matrix[0][6] - self.vpb_slices_at) * self.vpbRate_slice2 + (self.vpb_slices_at * self.vpbRate_slice1)
            
        else:
            matrix[0][7] = matrix[0][6] * self.vpbRate_slice1
            
        matrix[0][8] = matrix[0][6] - matrix[0][7]                                          # Kas - saldo
                
        ## REINVESTMENT / LIQUIDATION
        if matrix[0][8] > 0:                                                ## buy more equity if positive cash            
            matrix[0][9] = matrix[0][0] + matrix[0][8]                      ## kostprijs = start + aankoop
            matrix[0][10] = matrix[0][0] + matrix[0][3] + matrix[0][8]      ## marktwaarde = start + rendement + aankoop
            matrix[0][11] = matrix[0][1]                                    ## obligaties = ga verder met oude waarde
                
        elif (matrix[0][8] < 0) and (matrix[0][1] + matrix[0][8]) > 0:            
            matrix[0][9] = matrix[0][0]                                   ## kostprijs = start 
            matrix[0][10] = matrix[0][0] + matrix[0][3]                   ## marktwaarde = start + rendement 
            matrix[0][11] = matrix[0][1] + matrix[0][8]                  ## sell bonds if negative cash (if there's bonds)
            
        else:            
            matrix[0][9] = matrix[0][0] + matrix[0][8]                      ## kostprijs = start + aankoop
            matrix[0][10] = matrix[0][0] + matrix[0][3] + matrix[0][8]      ## marktwaarde = start + rendement minus verkocht
            matrix[0][11] = matrix[0][1]                                    ## obligaties = ga verder met oude waarde
        
        matrix[0][12] = matrix[0][2] * (1 + self.inflation)                 ## onroerend goed + inflatie
                            
        ## VPB DEFERRED
        matrix[0][13] = (matrix[0][10] + matrix[0][12]) - (matrix[0][9] + matrix[0][2]) ## stille reserve op aandelen + o/g
        
        if matrix[0][6] > self.vpb_slices_at:
            matrix[0][14] = matrix[0][13] * self.vpbRate_slice2
            
        elif (matrix[0][6] + matrix[0][13]) < self.vpb_slices_at:
            matrix[0][14] = matrix[0][13] * self.vpbRate_slice1 
            
        else:
            slice_1_margin = self.vpb_slices_at - matrix[0][6]
            matrix[0][14] = slice_1_margin * self.vpbRate_slice1 + (matrix[0][13] - slice_1_margin) * self.vpbRate_slice2
            
        ## AB CLAIM
        waarde = (matrix[0][10]+matrix[0][11]+matrix[0][12]-matrix[0][14])           ## werkelijk waarde min belasting latentie
        verkrijgingsprijs = (matrix[0][0]+matrix[0][1]+matrix[0][2])                ## oorspronkelijke investering
        
        if (waarde - verkrijgingsprijs) > self.box2_slices_at:
            matrix[0][15] = (waarde - verkrijgingsprijs - self.box2_slices_at)*self.box2Rate_slice2 + (self.box2_slices_at * self.box2Rate_slice1)
        else:
            matrix[0][15] = (waarde - verkrijgingsprijs)*self.box2Rate_slice1 
        
        ## METRICS
        matrix[0][16] = matrix[0][10] + matrix[0][11] + matrix[0][12]               ## marktwaarde assets
        matrix[0][17] = matrix[0][14] + matrix[0][15]                               ## Vpb + AB claim on exit
        matrix[0][18] = matrix[0][16] - matrix[0][17]                               ## netto opbrengst
        matrix[0][19] = matrix[0][7] + matrix[0][17]                                ## totale belasting (how to sum...)

        '''initialize rest of row of matrix'''        
        for i in range(matrix.shape[0]):

            if i > 0:
                
                ## INVESTMENTS & RETURNS
                matrix[i][0] = matrix[i-1][10]                                      # equity
                matrix[i][1] = matrix[i-1][11]                                      # bonds
                matrix[i][2] = matrix[i-1][12]                                      # property
                matrix[i][3] = matrix[i][0] * self.equity_return                    # return on equity
                matrix[i][4] = matrix[i][1] * self.bonds_return                     # return on bonds
                matrix[i][5] = matrix[i][2] * self.property_return                  # return on property (net rent)
                
                ## VPB CURRENT AND AFTER TAX CASH
                matrix[i][6] = matrix[i][4] + matrix[i][5] - self.bv_fees*(1+self.inflation)       # jaarwinst
                                                                                                    # Vpb current
                if matrix[i][6] > self.vpb_slices_at:                                               
                    matrix[i][7] = (matrix[i][6] - self.vpb_slices_at) * self.vpbRate_slice2 + (self.vpb_slices_at * self.vpbRate_slice1)
            
                else:
                    matrix[i][7] = matrix[i][6] * self.vpbRate_slice1
            
                matrix[i][8] = matrix[i][6] - matrix[i][7]                      # Kas - saldo

                ## REINVESTMENT / LIQUIDATION
                if matrix[i][8] > 0:                                                ## buy more equity if positive cash            
                    matrix[i][9] = matrix[i-1][9] + matrix[i][8]                      ## kostprijs = start + aankoop
                    matrix[i][10] = matrix[i][0] + matrix[i][3] + matrix[i][8]      ## marktwaarde = start + rendement + aankoop
                    matrix[i][11] = matrix[i][1]                                    ## obligaties = ga verder met oude waarde
                
                elif (matrix[i][8] < 0) and (matrix[i][1] + matrix[i][8]) > 0:            
                    matrix[i][9] = matrix[i-1][9]                                   ## kostprijs = start 
                    matrix[i][10] = matrix[i][0] + matrix[i][3]                   ## marktwaarde = start + rendement 
                    matrix[i][11] = matrix[i][1] + matrix[i][8]                  ## sell bonds if negative cash (if there's bonds)
                    
                else:            
                    matrix[i][9] = matrix[i-1][9] + matrix[i][8]                      ## kostprijs = start + aankoop
                    matrix[i][10] = matrix[i][0] + matrix[i][3] + matrix[i][8]      ## marktwaarde = start + rendement minus verkocht
                    matrix[i][11] = matrix[i][1]                                    ## obligaties = ga verder met oude waarde
                
                matrix[i][12] = matrix[i][2] * (1 + self.inflation)                 ## onroerend goed + inflatie
                
                ## VPB DEFERRED
                matrix[i][13] = (matrix[i][10] + matrix[i][12]) - (matrix[i][9] + matrix[0][2]) ## stille reserve op aandelen + o/g
        
                if matrix[i][6] > self.vpb_slices_at:
                    matrix[i][14] = matrix[i][13] * self.vpbRate_slice2
            
                elif (matrix[i][6] + matrix[i][13]) < self.vpb_slices_at:
                    matrix[i][14] = matrix[i][13] * self.vpbRate_slice1 
            
                else:
                    slice_1_margin = self.vpb_slices_at - matrix[i][6]
                    matrix[i][14] = slice_1_margin * self.vpbRate_slice1 + (matrix[i][13] - slice_1_margin) * self.vpbRate_slice2
            
                ## AB CLAIM
                waarde = (matrix[i][10]+matrix[i][11]+matrix[i][12]-matrix[i][14])           ## werkelijk waarde min belasting latentie
                verkrijgingsprijs = (matrix[0][0]+matrix[0][1]+matrix[0][2])                ## oorspronkelijke investering
        
                if (waarde - verkrijgingsprijs) > self.box2_slices_at:
                    matrix[i][15] = (waarde - verkrijgingsprijs - self.box2_slices_at)*self.box2Rate_slice2 + (self.box2_slices_at * self.box2Rate_slice1)
                else:
                    matrix[i][15] = (waarde - verkrijgingsprijs)*self.box2Rate_slice1 
        
                ## METRICS
                matrix[i][16] = matrix[i][10] + matrix[i][11] + matrix[i][12]               ## marktwaarde assets
                matrix[i][17] = matrix[i][14] + matrix[i][15]                               ## Vpb + AB claim on exit
                matrix[i][18] = matrix[i][16] - matrix[i][17]                               ## netto opbrengst
                
                sum_of_matrix = np.sum(matrix, axis=0)                                      ## sum all columns
                sum_of_current_tax = sum_of_matrix[7]                                       ## pick the 'current tax' column
                matrix[i][19] = sum_of_current_tax + matrix[i][17]                          ## totale belasting (how to sum...)
            
        output = pd.DataFrame(matrix, columns=
                              ['Aandelen','Obligaties','Vastgoed','Rndmnt_Aandelen','Rndmt_Obligaties','Rndmnt_Vastgoed', 'Jaarwinst', 'Vpb_current',
                               'Kas', 'Kostprijs_Aandelen', 'Marktwaarde_Aandelen', 'Marktwaarde_Obligaties', 'Marktwaarde_Vastgoed', 'Stille_reserve', 'Vpb_deferred', 'AB_claim', 'Portefeuille_Box2',
                               'ExitTax_Box2', 'Netto_Box2', 'Cum_Tax_Box2'])
                
        return output
    
    def _box3_calc(self):
        
        matrix = np.zeros((self.term, 18), dtype=float)

        '''initialize first row of matrix'''
        
        ## INVESTMENTS & RETURNS
        matrix[0][0] = self.equity                                                         # equity
        matrix[0][1] = self.bonds                                                          # bonds
        matrix[0][2] = self.property                                                       # property
        matrix[0][3] = matrix[0][0] * self.equity_return                                   # return on equity
        matrix[0][4] = matrix[0][1] * self.bonds_return                                    # return on bonds
        matrix[0][5] = matrix[0][2] * self.property_return                                 # return on property (net rent)
        
        ## BOX3 CURRENT AND AFTER TAX CASH
        matrix[0][6] = matrix[0][3] + matrix[0][4] + matrix[0][5]    # Box 3 inkomen
                                                                                          # Box 3 belasting current
        if matrix[0][6] > 0:                                               
            matrix[0][7] = (matrix[0][6] - self.box3_freezone) * self.box3Rate
            
        else:
            matrix[0][7] = 0 
                        
        matrix[0][8] = matrix[0][4] + matrix[0][5] - matrix[0][7]           # Kas - saldo
                
        ## REINVESTMENT / LIQUIDATION                
        if matrix[0][8] > 0:                                                ## buy more equity if positive cash            
            matrix[0][9] = matrix[0][0] + matrix[0][3] + matrix[0][8]      ## marktwaarde = start + rendement + aankoop
            matrix[0][10] = matrix[0][1]                                    ## obligaties = ga verder met oude waarde
                
        elif (matrix[0][8] < 0) and (matrix[0][1] + matrix[0][8]) > 0:            
            matrix[0][9] = matrix[0][0] + matrix[0][3]                   ## marktwaarde = start + rendement 
            matrix[0][10] = matrix[0][1] + matrix[0][8]                  ## sell bonds if negative cash (if there's bonds)
            
        else:            
            matrix[0][9] = matrix[0][0] + matrix[0][3] + matrix[0][8]      ## marktwaarde = start + rendement minus verkocht
            matrix[0][10] = matrix[0][1]                                    ## obligaties = ga verder met oude waarde
        
        matrix[0][11] = matrix[0][2] * (1 + self.inflation)                 ## onroerend goed + inflatie
                                          
        ## BOX 3 DEFERRED
        matrix[0][12] = (matrix[0][11] - matrix[0][2])               ## stille reserve op o/g
        matrix[0][13] = matrix[0][12] * self.box3Rate
        
        ## METRICS
        matrix[0][14] = matrix[0][9] + matrix[0][10] + matrix[0][11]               ## marktwaarde assets
        matrix[0][15] = matrix[0][13]                                               ## Vpb + AB claim on exit
        matrix[0][16] = matrix[0][14] - matrix[0][15]                               ## netto opbrengst
        matrix[0][17] = matrix[0][7] + matrix[0][13]                                ## totale belasting (how to sum...)

        '''initialize rest of row of matrix'''        
        for i in range(matrix.shape[0]):

            if i > 0:
                
                ## INVESTMENTS & RETURNS
                matrix[i][0] = matrix[i-1][9]                                  # equity
                matrix[i][1] = matrix[i-1][10]                                  # bonds
                matrix[i][2] = matrix[i-1][11]                                  # property
                matrix[i][3] = matrix[i][0] * self.equity_return                # return on equity
                matrix[i][4] = matrix[i][1] * self.bonds_return                 # return on bonds
                matrix[i][5] = matrix[i][2] * self.property_return              # return on property (net rent)
                
                ## BOX3 CURRENT AND AFTER TAX CASH
                matrix[i][6] = matrix[i][3] + matrix[i][4] + matrix[i][5]        # Box 3 inkomen
                                                                                                # Box 3 belasting current
                if matrix[i][6] > 0:                                               
                    matrix[i][7] = (matrix[i][6] - self.box3_freezone) * self.box3Rate
                    
                else:
                    matrix[i][7] = 0 
                                
                matrix[i][8] = matrix[i][4] + matrix[i][5] - matrix[i][7]           # Kas - saldo
                        
                ## REINVESTMENT / LIQUIDATION
                          
                if matrix[i][8] > 0:                                                ## buy more equity if positive cash
                    matrix[i][9] = matrix[i][0] + matrix[i][3] + matrix[i][8]      ## marktwaarde = start + rendement + aankoop
                    matrix[i][10] = matrix[i][1]                                    ## obligaties = ga verder met oude waarde
                        
                elif (matrix[i][8] < 0) and (matrix[i][1] + matrix[i][8]) > 0:
                    matrix[i][9] = matrix[i][0] + matrix[i][3]                   ## marktwaarde = start + rendement 
                    matrix[i][10] = matrix[i][1] + matrix[i][8]                     ## sell bonds if negative cash (if there's bonds)
                    
                else:
                    matrix[i][9] = matrix[i][0] + matrix[i][3] + matrix[i][8]      ## marktwaarde = start + rendement minus verkocht
                    matrix[i][10] = matrix[i][1]                                    ## obligaties = ga verder met oude waarde
                     
                matrix[i][11] = matrix[i][2] * (1 + self.inflation)                 ## onroerend goed + inflatie
                    
                ## BOX 3 DEFERRED
                matrix[i][12] = (matrix[i][11] - matrix[0][2])               ## stille reserve op o/g
                matrix[i][13] = matrix[i][12] * self.box3Rate
                
                ## METRICS
                matrix[i][14] = matrix[i][9] + matrix[i][10] + matrix[i][11]               ## marktwaarde assets
                matrix[i][15] = matrix[i][13]                                               ## Box 3
                matrix[i][16] = matrix[i][14] - matrix[i][15]                               ## netto
                
                sum_of_matrix = np.sum(matrix, axis=0)                                      ## sum all columns
                sum_of_current_tax = sum_of_matrix[7]                                       ## pick the 'current tax' column
                matrix[i][17] = sum_of_current_tax + matrix[i][15]                          ## totale belasting (how to sum...)
                            
        output = pd.DataFrame(matrix, columns=
                              ['Aandelen','Obligaties','Vastgoed','Rndmnt_Aandelen','Rndmt_Obligaties','Rndmnt_Vastgoed', 'Box3_Inkomen', 'Box3_Belasting',
                               'Kas', 'Marktwaarde_Aandelen', 'Marktwaarde_Obligaties', 'Marktwaarde_Vastgoed', 'Stille_reserve', 'Box3_deferred', 'Portefeuille_Box3',
                               'ExitTax_Box3', 'Netto_Box3', 'Cum_Tax_Box3'])
                
        return output

    def output(self):
        
        box_2 = self._box2_calc()[['Portefeuille_Box2', 'ExitTax_Box2', 'Netto_Box2', 'Cum_Tax_Box2']]
        box_3 = self._box3_calc()[['Portefeuille_Box3', 'ExitTax_Box3', 'Netto_Box3', 'Cum_Tax_Box3']]
        
        output = pd.concat([box_2, box_3], axis = 1)
        cols = ['Portefeuille_Box2', 'ExitTax_Box2', 'Netto_Box2', 'Portefeuille_Box3', 'ExitTax_Box3', 'Netto_Box3', 'Cum_Tax_Box2', 'Cum_Tax_Box3']
        
        output[cols].astype('int')
        
        output['Jaar'] = np.arange(len(output)) ## add column with years
        output.set_index('Jaar', inplace=True)

        return output
    
