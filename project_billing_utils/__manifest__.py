##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

{
    'name': 'Analytic and project wizard for service companies',
    'version': '11.0.1.0.0',
    'category': 'Generic Modules/Projects & Services',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'website': 'https://www.camptocamp.com',
    'depends': ['project',
                'hr_timesheet',
                'account',
                'sale_timesheet'],
    'license': 'AGPL-3',
    'data': [
        'views/invoice_view.xml',
        'views/project_view.xml',
        'wizard/associate_aal_view.xml',
        'wizard/dissociate_aal_view.xml',
        'wizard/open_invoices_view.xml',
        'wizard/blank_invoice_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
