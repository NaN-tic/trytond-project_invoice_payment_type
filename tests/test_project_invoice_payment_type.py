# This file is part project_invoice_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import doctest_setup, doctest_teardown
from trytond.tests.test_tryton import doctest_checker


class ProjectInvoicePaymentTypeTestCase(ModuleTestCase):
    'Test Project Invoice Payment Type module'
    module = 'project_invoice_payment_type'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProjectInvoicePaymentTypeTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_project_invoice_payment_type.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
