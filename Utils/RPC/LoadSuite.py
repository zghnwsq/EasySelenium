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
        for i in li:
            suite.addTest(test_class('test_%s_%s' % (mtd, str(i))))
    else:
        raise Exception('Input args required: Test Method  [Data Source Range]')
    return suite


