'''
302 Pair Programming Assignment
Salaries Tax Calculator - unittesting
-----
Created by: Chen Tak Hei, Tsang Yung
Last Modified: March 23, 2022
'''
import sys
import unittest
import tax as t

class Testclass(unittest.TestCase):
    # test mpf fuction if input below 85200, would produce 0
    def test_case1(var):
        var.assertEqual(t.MPF(85199), 0, "Error: MPF() should produce 0 when input below 85200.")
    
    #test mpf function if input is above 85200, below 360000, would produce input*0.05
    def test_case2(var):
        var.assertEqual(t.MPF(200000), 10000, "Error: MPF() should produce 'input*0.05' when input is above 85200 and below 360000.")

    #test mpf function if input is above 360000, would produce 18000
    def test_case3(var):
        var.assertEqual(t.MPF(360001), 18000, "Error: MPF() should produce 18000, when input is above 360000.")

    #test net_income function would produce input - MPF(input)
    def test_case4(var):
        var.assertEqual(t.net_income(139000), 132050, "Error: net_income should produce input - MPF(input)")

    #test NCI() would produce input - 132000, when separate assesment is assumed, i.e. joint = False
    def test_case5(var):
        var.assertEqual(t.NCI(132050), 50, "Error: NCI() should produce input - 132000, when separate assesment is assumed, i.e. joint = False")        

    #test NCI() would produce input - 264000, when joint assesment is assumed, i.e. joint = True
    def test_case6(var):
        var.assertEqual(t.NCI(264100, True), 100, "Error: NCI() should produce input - 264000, when joint assesment is assumed, i.e. joint = True")  
  
    #test tax_band() would produce input * 0.02, when input <= 50000
    def test_case7(var):
        var.assertEqual(t.tax_band(49999), 999, "Error: tax_band() should produce input * 0.02, when input <= 50000")

    #test tax_band() would produce 1000 + (input - 50000) * 0.06, when 50001 <= input <= 100000
    def test_case8(var):
        var.assertEqual(t.tax_band(99999), 3999, "Error: tax_band() should produce 1000 + (input - 50000) * 0.06, when 50001 <= input <= 100000")

    #test tax_band() would produce 4000 + (input - 100000) * 0.1, when 100001 <= input <= 150000 
    def test_case8(var):
        var.assertEqual(t.tax_band(149999), 8999, "Error: tax_band() should produce 4000 + (input - 100000) * 0.1, when 100001 <= input <= 150000")

    #test tax_band() would produce 9000 + (input - 150000) * 0.14, when 150001 <= input <= 200000
    def test_case9(var):
        var.assertEqual(t.tax_band(199999), 15999, "Error: tax_band() should 9000 + (input - 150000) * 0.14, when 150001 <= input <= 200000")

    #test tax_band() would produce 16000 + (input - 200000) * 0.17, when 200001 <= input < 3144000 
    def test_case10(var):
        var.assertEqual(t.tax_band(249999), 24499, "Error: tax_band() should produce 16000 + (input - 200000) * 0.17, when 200001 <= input < 3144000") 

    #test tax_band() would produce input * 0.15, when 3144000 <= input
    def test_case10(var):
        var.assertEqual(t.tax_band(3144001), 471600, "Error: tax_band() should produce input * 0.15, when 3144000 <= input")

    #standard_tax() would produce input * 0.15
    def test_case11(var):
        var.assertEqual(t.standard_tax(3144001), 471600, "Error: standard_tax() should produce input * 0.15")

    #tax_calc() would compare with the output under progressive tax calculation and standard tax calculation,then produce a smaller output 
    def test_case12(var):
        var.assertEqual(t.tax_calc(132050), 1, "Error: tax_calc() should produce a smaller output by comparing the progressive tax calculation and standard tax calculation")

    #tax_calc() would compare with the output under progressive tax calculation and standard tax calculation,then produce a smaller output
    def test_case13(var):
        var.assertEqual(t.tax_calc(482006, joint = True), 19061, "Error: tax_calc() should produce a smaller output by comparing the progressive tax calculation and standard tax calculation")

    #tax_calc() would compare with the output under progressive tax calculation and standard tax calculation,then produce a smaller output
    def test_case14(var):
        var.assertEqual(t.tax_calc(1722000), 252300, "Error: tax_calc() should produce a smaller output by comparing the progressive tax calculation and standard tax calculation")

    #tax_calc() would compare with the output under progressive tax calculation and standard tax calculation,then produce a smaller output 
    def test_case15(var):
        var.assertEqual(t.tax_calc(3294000, joint = True), 494100, "Error: tax_calc() should produce a smaller output by comparing the progressive tax calculation and standard tax calculation")

if __name__ == "__main__":
    unittest.main()
