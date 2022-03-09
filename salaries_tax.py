def MPF(total_income):
    """
    Calculate the amount of MPF mandatory contribution based on husband's and wife's personal income
    """
    # rounding the total income to 0 decimal place
    income = round(total_income)     
    # if annual income is below $85200, the amount of MPF contribution is 0.
    if total_income < 85200:        
        return 0
    # round mpf to zero decimal places
    total_income = int(round(total_income * 0.05))
    return min(18000, total_income)
        
def net_income(total_income):
    """
    Calculate the net total income after MPF deduction
    """
    total_income = int(total_income - MPF(total_income))
    return total_income

def NCI(net_income, joint = False):
    """
    Calculate the Net Chargeable Income (after deducting Tax Allowance)
    """
    net_income = int(net_income)
    if net_income < 3144000:
        # The allowance is 132000 if separated assessment is assumed.
        allowance = 132000               
        if joint:
            # The allowance is 264000 if joint assessment is assumed.
            allowance *= 2               
        net_income = int(net_income - allowance)
    return max(net_income, 0)

def tax_band(nci):
    """
    Calculate the tax payable while considering different tax bands.
    """
    # Calculate under Progressive Tax rates
    if nci <= 50000:                 
        nci = int(nci * 0.02)
        return nci
    # First Tax bracket
    elif 50001 <= nci <= 100000:     
        nci = int(1000 + (nci - 50000) * 0.06)
        return nci
    # Second Tax bracket
    elif 100001 <= nci <= 150000:    
        nci = int(4000 + (nci - 100000) * 0.1)
        return nci
    # Third Tax bracket
    elif 150001 <= nci <= 200000:    
        nci = int(9000 + (nci - 150000) * 0.14)
        return nci
    # Fourth (remainder) Tax bracket
    elif 200001 <= nci < 3144000:    
        nci = int(16000 + (nci - 200000) * 0.17)
        return nci
    # Calculate under Standard Tax rate
    elif 3144000 <= nci:             
        nci = int(nci * 0.15)
        return nci

def standard_tax(net_income, joint = False):
    """
    Calculate the Tax Payable using standard tax rate using net income before deducting allowance
    """
    net_income = int(net_income)
    standard_tax_rate = 0.15              
    net_income = int(net_income * standard_tax_rate)
    return max(net_income, 0)


def tax_calc(net_income, joint = False):
    """
    Separated assessment and Joint assessment calculation
    """

    if standard_tax(net_income) < tax_band(NCI(net_income)):
        tax_payable = standard_tax(net_income)
        return int(tax_payable)  
    
    elif standard_tax(net_income) >= tax_band(NCI(net_income)):
        tax_payable = tax_band(NCI(net_income, joint))
        return int(tax_payable)  

def tax_output(data):
    """
    Generate output data: 
    (1) Calculated MPF mandatory contribution based on personal income (using output["husband_mpf"], output["wife_mpf"], type: int)
    (2) Salaries Tax to be paid if separate assessment assumed (using output["husband_tax"], output["wife_tax"], type: int)
    (3) Salaries Tax to be paid if joint assessment assumed (using output["joint_tax"], type: int)
    (4) Recommendation: whether joint assessment should be recommended (using output["joint"], type: bool)
    """
    output = {
        "husband_tax": 0,
        "husband_mpf": MPF(data["husband_income"]),
        "wife_tax": 0,
        "wife_mpf": MPF(data["wife_income"]),
        "joint_tax": 0,
        "joint": False,
    }
    output["husband_tax"] = tax_calc(net_income(data["husband_income"]))
    output["wife_tax"]  = tax_calc(net_income(data["wife_income"]))
    output["joint_tax"] = tax_calc(net_income(data["husband_income"]) + net_income(data["wife_income"]), joint = True)
    output["joint"] = (output["husband_tax"] + output["wife_tax"]) > output["joint_tax"]
    return output
    
def get_input():
    """
    Collect input data (Husband's and wife's personal annual income)
    """
    data = {
        "husband_income": 0,
        "wife_income": 0,
    }

    def income(role):
        personal_income = int(input("Please type in %s annual income: " % role))
        if personal_income < 0:   
        # raise Error#1: if any inputted income is below $0, raise ValueError and prompt error message.  
            raise ValueError("Please rerun the program and type in the correct annual income. The salary should not be below $0.")
        return personal_income

    data["husband_income"] = income("Husband's")
    data["wife_income"] = income("Wife's")
    
    return data                        

def show_output(result):
    """
    print output data: 
    (1) Calculated MPF mandatory contribution based on personal income (in line 89, 91)
    (2) Salaries Tax to be paid if separate assessment assumed (in line 90, 92)
    (3) Salaries Tax to be paid if joint assessment assumed (in line 93)
    (4) Recommendation: whether joint assessment should be recommended (in line 94)
    """
    print ("\nThe amount of MPF mandatory contribution based on husband's personal income is $%s.\n" % '{:,}'.format(result["husband_mpf"]))
    print ("The amount of Salaries Tax payable by husband if separate assessment assumed is $%s.\n" % '{:,}'.format(result["husband_tax"]))
    print ("The amount of MPF mandatory contribution based on wife's personal income is $%s.\n" % '{:,}'.format(result["wife_mpf"]))
    print ("The amount of Salaries Tax payable by wife if separate assessment assumed is $%s.\n" % '{:,}'.format(result["wife_tax"]))
    print ("The amount of Salaries Tax payable if joint assessment assumed is $%s.\n" % '{:,}'.format(result["joint_tax"]))
    print ("Should joint assessment be recommended? %s" % ("Yes, joint assessment is recommended." if result["joint"] else "No, joint assessment is not recommended."))

if __name__ == "__main__":
    print (
"""
Salaries Tax Computation                                                                                                                                     
Based on requirements from Hong Kong Inland Revenue Department (HKIRD)            
Year of Assessment: 2021/22                                                      
Martial Status: Married (Default)\n""")
    data = get_input()
    result = tax_output(data)
    show_output(result)
