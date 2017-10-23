=====================================
Project Invoice Payment Type Scenario
=====================================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_chart, \
    ...     get_accounts
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     create_payment_term
    >>> today = datetime.date.today()

Create database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install project_invoice_payment_type::

    >>> Module = Model.get('ir.module')
    >>> sale_module, = Module.find([('name', '=', 'project_invoice_payment_type')])
    >>> sale_module.click('install')
    >>> Wizard('ir.module.install_upgrade').execute('upgrade')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Reload the context::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> config._context = User.get_preferences(True, config.context)

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create payment type::

    >>> PaymentType = Model.get('account.payment.type')
    >>> payment_type = PaymentType(name='Receivable', kind='receivable')
    >>> payment_type.save()

Create customer::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.customer_payment_term = payment_term
    >>> customer.customer_payment_type = payment_type
    >>> customer.save()

Create employee::

    >>> Employee = Model.get('company.employee')
    >>> employee = Employee()
    >>> party = Party(name='Employee')
    >>> party.save()
    >>> employee.party = party
    >>> employee.company = company
    >>> employee.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> hour, = ProductUom.find([('name', '=', 'Hour')])
    >>> Product = Model.get('product.product')
    >>> ProductTemplate = Model.get('product.template')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'Service'
    >>> template.default_uom = hour
    >>> template.type = 'service'
    >>> template.list_price = Decimal('20')
    >>> template.cost_price = Decimal('5')
    >>> template.account_revenue = revenue
    >>> template.save()
    >>> product.template = template
    >>> product.save()

Create a Project::

    >>> ProjectWork = Model.get('project.work')
    >>> TimesheetWork = Model.get('timesheet.work')
    >>> project = ProjectWork()
    >>> project.name = 'Test effort'
    >>> work = TimesheetWork()
    >>> work.name = 'Test effort'
    >>> work.save()
    >>> project.work = work
    >>> project.type = 'project'
    >>> project.party = customer
    >>> project.project_invoice_method = 'effort'
    >>> project.product = product
    >>> project.effort_duration = datetime.timedelta(hours=1)
    >>> task = ProjectWork()
    >>> task.name = 'Task 1'
    >>> work = TimesheetWork()
    >>> work.name = 'Task 1'
    >>> work.save()
    >>> task.work = work
    >>> task.type = 'task'
    >>> task.product = product
    >>> task.effort_duration = datetime.timedelta(hours=5)
    >>> project.children.append(task)
    >>> project.save()
    >>> task, = project.children

Check project duration::

    >>> project.reload()
    >>> project.invoiced_duration
    datetime.timedelta(0)
    >>> project.duration_to_invoice
    datetime.timedelta(0)
    >>> project.invoiced_amount
    Decimal('0')

Do 1 task::

    >>> task.state = 'done'
    >>> task.save()

Check project duration::

    >>> project.reload()
    >>> project.invoiced_duration
    datetime.timedelta(0)
    >>> project.duration_to_invoice
    datetime.timedelta(0, 18000)
    >>> project.invoiced_amount
    Decimal('0')

Invoice project::

    >>> project.click('invoice')
    >>> project.invoiced_duration
    datetime.timedelta(0, 18000)
    >>> project.duration_to_invoice
    datetime.timedelta(0)
    >>> project.invoiced_amount
    Decimal('100.00')

Invoice::

    >>> Invoice = Model.get('account.invoice')
    >>> invoice, = Invoice.find([])
    >>> invoice.payment_type == payment_type
    True
