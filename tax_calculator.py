def MPF(total_income):
    income = round(total_income)
    if total_income < 85200:
        return 0
    return round(min(18000, total_income * 0.05))
        
def net_income(total_income):
    total_income = round(total_income)
    return round(total_income - MPF(total_income))

def NCI(net_income, combined = False):
    allowance = 132000
    if combined:
        allowance *= 2
    return max(net_income - allowance, 0)

def tax_band(nci):
    if nci <= 50000:
        return int(round(nci * 0.02))
    elif 50001 <= nci <= 100000:
        return int(round(1000 + (nci - 50000) * 0.06))
    elif 100001 <= nci <= 150000:
        return int(round(4000 + (nci - 100000) * 0.1))
    elif 150001 <= nci <= 200000:
        return int(round(9000 + (nci - 150000) * 0.14))
    elif 200001 <= nci < 3144000:	
        return int(round(16000 + (nci - 200000) * 0.17))
    elif 3144000 <= nci:
        return int(round(nci * 0.15))

def tax_calc_process(net_income, combined = False):
    tax_payment = tax_band(NCI(net_income, combined))

    return int(tax_payment)

def tax_output(data):
    output = {
        "combined": False,
        "husband_tax": 0,
        "husband_mpf": MPF(data["husband_income"]),
        "wife_tax": 0,
        "wife_mpf": MPF(data["wife_income"]),
        "combined_tax": 0,
    }
    output["husband_tax"] = tax_calc_process(net_income(data["husband_income"]))
    output["wife_tax"]  = tax_calc_process(net_income(data["wife_income"]))
    output["combined_tax"] = tax_calc_process(net_income(data["husband_income"]) + net_income(data["wife_income"]), combined = True)
    output["combined"] = (output["husband_tax"] + output["wife_tax"]) > output["combined_tax"]
    return output
    
def get_input():
    data = {
        "husband_income": 0,
        "wife_income": 0,
    }

    def income(role):
        return int(input("Please type in %s annual income: " % role))

    data["husband_income"] = income("Husband's")
    data["wife_income"] = income("Wife's")

    return data

def show_output(result):
    print ("\nThe amount of MPF mandatory contribution based on husband's personal income is $%d.\n" % result["husband_mpf"])
    print ("The amount of Salaries Tax payable by husband if separate assessment assumed is $%d.\n" % result["husband_tax"])
    print ("The amount of MPF mandatory contribution based on wife's personal income is $%d.\n" % result["wife_mpf"])
    print ("The amount of Salaries Tax payable by wife if separate assessment assumed is $%d.\n" % result["wife_tax"])
    print ("The amount of Salaries Tax payable if joint assessment assumed is $%d.\n" % result["combined_tax"])
    print ("Should joint assessment be recommended? %s" % ("Yes, joint assessment is recommended." if result["combined"] else "No, joint assessment is not recommended."))

if __name__ == "__main__":
    print ("Tax Calculator")
    data = get_input()
    result = tax_output(data)
    show_output(result)
