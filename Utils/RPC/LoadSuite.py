import unittest
from Utils.Runner.Cmd import get_range


def load_suite(test_class, mtd=None, rg=None):
    suite = unittest.TestSuite()
    if not mtd and not rg:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    elif 'all' in mtd:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    elif mtd and rg:
        li = get_range(rg)
        count = unittest.TestLoader().loadTestsFromTestCase(test_class).countTestCases()
        formatter = f'test_%s_%0{len(str(count))}d'
        for i in li:
            suite.addTest(test_class(formatter % (mtd, i)))
    elif mtd:
        suite.addTest(test_class(f'test_{mtd}'))
    else:
        raise Exception('Input args required: Test Method')
    return suite


