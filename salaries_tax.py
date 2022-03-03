def MPF(total_income):
    """
    Calculate the amount of MPF mandatory contribution based on husband's and wife's personal income
    """
    income = round(total_income)     # rounding the total income to 0 decimal place
    if total_income < 85200:         # if annual income is below $85200, the amount of MPF contribution is 0.
        return 0
    total_income = int(round(total_income * 0.05))
    return min(18000, total_income)
        
def net_income(total_income):
    """
    Calculate the net total income after MPF deduction
    """
    total_income = int(round(total_income - MPF(total_income)))
    return total_income

def NCI(net_income, joint = False):
    """
    Calculate the Net Chargeable Income (after deducting Tax Allowance)
    """
    net_income = int(net_income)
    allowance = 132000               #132000 if separated assessment is assumed.
    if joint:
        allowance *= 2               #264000 if joint assessment is assumed.
    net_income = int(round(net_income - allowance))
    return max(net_income, 0)

def tax_band(nci):
    """
    Calculate the tax payable while considering different tax bands.
    """
    if nci <= 50000:                 # Calculate under Progressive Tax rates
        nci = int(round(nci * 0.02))
        return nci
    elif 50001 <= nci <= 100000:     # First Tax bracket
        nci = int(round(1000 + (nci - 50000) * 0.06))
        return nci
    elif 100001 <= nci <= 150000:    # Second Tax bracket
        nci = int(round(4000 + (nci - 100000) * 0.1))
        return nci
    elif 150001 <= nci <= 200000:    # Third Tax bracket
        nci = int(round(9000 + (nci - 150000) * 0.14))
        return nci
    elif 200001 <= nci < 3144000:    # Fourth (remainder) Tax bracket
        nci = int(round(16000 + (nci - 200000) * 0.17))
        return nci
    elif 3144000 <= nci:             # Calculate under Standard Tax rate
        nci = int(round(nci * 0.15))
        return nci

def standard_tax(net_income, joint = False):
    """
    Calculate the Tax Payable using standard tax rate using net income before deducting allowance
    """
    net_income = int(net_income)
    standard_tax_rate = 0.15              
    net_income = int(round(net_income * standard_tax_rate))
    return max(net_income, 0)


def tax_calc(net_income, joint = False):
    """
    Separated assessment and Joint assessment calculation
    """
    if net_income < 3144000:
        if standard_tax(net_income) < tax_band(NCI(net_income)):
            tax_payable = standard_tax(net_income)
            return int(tax_payable)  
        tax_payable = tax_band(NCI(net_income, joint))
        return int(tax_payable)  
    tax_payable = tax_band(NCI(net_income, joint))
    return int(tax_payable)          # the tax payable calculated should be in integer type.  

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
        if personal_income < 0:     # Error#1: if any inputted income is below $0, raise ValueError and prompt error message.
            raise ValueError("Please rerun the program and type in the correct annual income. The salary should not be below $0.")
        return personal_income

    data["husband_income"] = income("Husband's")
    data["wife_income"] = income("Wife's")
    
    return data                        # inputted data store in data

def show_output(result):
    """
    print output data: 
    (1) Calculated MPF mandatory contribution based on personal income (in line 89, 91)
    (2) Salaries Tax to be paid if separate assessment assumed (in line 90, 92)
    (3) Salaries Tax to be paid if joint assessment assumed (in line 93)
    (4) Recommendation: whether joint assessment should be recommended (in line 94)
    """
    print ("\nThe amount of MPF mandatory contribution based on husband's personal income is $%d.\n" % result["husband_mpf"])
    print ("The amount of Salaries Tax payable by husband if separate assessment assumed is $%d.\n" % result["husband_tax"])
    print ("The amount of MPF mandatory contribution based on wife's personal income is $%d.\n" % result["wife_mpf"])
    print ("The amount of Salaries Tax payable by wife if separate assessment assumed is $%d.\n" % result["wife_tax"])
    print ("The amount of Salaries Tax payable if joint assessment assumed is $%d.\n" % result["joint_tax"])
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
