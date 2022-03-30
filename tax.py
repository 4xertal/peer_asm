'''
302 Pair Programming Assignment
Salaries Tax Calculator 
-----
Created by: Chen Tak Hei, Tsang Yung
Last Modified: March 23, 2022
'''
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
    standard_tax_payable = standard_tax(net_income)
    progressive_tax_payable = tax_band(NCI(net_income, joint))
    payable = int(min(standard_tax_payable, progressive_tax_payable))
    return max(payable, 0)

def tax_output(data):
    """
    Generate output data: 
    (1) Calculated MPF mandatory contribution based on personal income (using output["husband_mpf"], output["wife_mpf"], type: int)
    (2) Salaries Tax to be paid if separate assessment assumed (using output["husband_tax"], output["wife_tax"], type: int)
    (3) Salaries Tax to be paid if joint assessment assumed (using output["joint_tax"], type: int)
    (4) Recommendation: whether joint assessment should be recommended (using output["joint"], type: bool)
    (5) Total amount of tax payble(using output(["total_tax"], type: int))
    (6) Tax reduction implemented (using output["husband_tax_after_reduction"], output["wife_tax_after_reduction"], and output["joint_tax_after_reduction"]) 
    """
    output = {
        "husband_tax": 0,
        "husband_mpf": MPF(data["husband_income"]),
        "wife_tax": 0,
        "wife_mpf": MPF(data["wife_income"]),
        "joint_tax": 0,
        "joint": False,
        "total_tax": 0,
        "husband_tax_after_reduction": 0,
        "wife_tax_after_reduction": 0,
        "joint_tax_after_reduction": 0,
    }
    output["husband_tax"] = tax_calc(net_income(data["husband_income"]))
    output["wife_tax"]  = tax_calc(net_income(data["wife_income"]))
    output["joint_tax"] = tax_calc(net_income(data["husband_income"]) + net_income(data["wife_income"]), joint = True)
    output["joint"] = (output["husband_tax"] + output["wife_tax"]) > output["joint_tax"]
    output["total_tax"] = tax_calc(net_income(data["husband_income"])) + tax_calc(net_income(data["wife_income"]))
    output["husband_tax_after_reduction"] = max(output["husband_tax"]-10000, 0)
    output["wife_tax_after_reduction"] = max(output["wife_tax"]-10000, 0)
    output["joint_tax_after_reduction"] = max(output["joint_tax"]-10000, 0)
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
    (1) Calculated MPF mandatory contribution based on personal income
    (2) Salaries Tax to be paid before tax reduction if separate assessment assumed
    (3) Salaries Tax to be paid if joint assessment assumed
    (4) Total amount of Salaries Tax payable by husband and wife if seperate assessment is assumed 
    (5) Recommendation: whether joint assessment should be recommended
    (6) Salaries Tax to be paid after tax reduction if seperate assessment is assumed
    (7) Salaries Tax to be paid after tax reduction if joint assessment is assumed
    """
    print ("\n" + "="*50 + "\n(a) Calculated MPF mandatory contribution based on personal income\n" + "\nHusband's Mandatory MPF Contribution: $%s.\n" % '{:,}'.format(result["husband_mpf"]))
    print ("Wife's Mandatory MPF Contribution: $%s.\n" % '{:,}'.format(result["wife_mpf"]))
    print ("-"*50 + "\n(b.i) Salaries Tax to be paid if separate assessment assumed (before tax reduction)\n" +"\nHusband's Salaries Tax payable: $%s.\n" % '{:,}'.format(result["husband_tax"]))
    print ("Wife's Salaries Tax payable: $%s.\n" % '{:,}'.format(result["wife_tax"]))
    print ("Total Salaries Tax payable: $%s.\n" % '{:,}'.format(result["total_tax"]))
    print ("-"*50 + "\n(c.i) Salaries Tax to be paid if joint assessment assumed (before tax reduction)\n" + "\nTotal Salaries Tax payable: $%s.\n" % '{:,}'.format(result["joint_tax"]))
    print ("-"*50 + "\n(d) Recommendation: whether joint assessment should be recommended\n" +"\nShould joint assessment be recommended? %s.\n" % ("\n-> Yes, joint assessment is recommended" if result["joint"] else "\n-> No, joint assessment is not recommended"))
    if result["joint"]:
        print ("-"*50 + "\n(c.ii) Salaries Tax to be paid if joint assessment assumed (after tax reduction)\n" + "\nTotal Salaries Tax payable: $%s.\n" % '{:,}'.format(result["joint_tax_after_reduction"]))
        print ("="*50)
    else:
        print ("-"*50 + "\n(b.ii) Salaries Tax to be paid if separate assessment assumed (after tax reduction)\n" +"\nHusband's Salaries Tax payable: $%s.\n" %'{:,}'.format(result["husband_tax_after_reduction"]))
        print ("Wife's Salaries Tax payable: $%s.\n" %'{:,}'.format(result["wife_tax_after_reduction"]))
        print("="*50)

if __name__ == "__main__":
    print (
"""
Salaries Tax Computation                                                                                                                                     
Based on requirements from Hong Kong Inland Revenue Department (HKIRD)            
Year of Assessment: 2021/22, Per 2022-23 Budget Proposals                                                      
Martial Status: Married (By default)\n""")
    data = get_input()
    result = tax_output(data)
    show_output(result)
