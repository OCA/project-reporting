# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Analytic and project wizard for service companies',
    'version': '8.0.1.4.0',
    'category': 'Generic Modules/Projects & Services',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'website': 'http://www.camptocamp.com',
    'depends': ['project',
                'hr_timesheet_invoice',
                'project_analytic_line_view'],
    'data': [
        'invoice_view.xml',
        'project_view.xml',
        'wizard/associate_aal_view.xml',
        'wizard/dissociate_aal_view.xml',
        'wizard/open_invoices_view.xml',
        'wizard/blank_invoice_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
