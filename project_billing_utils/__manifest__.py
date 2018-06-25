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
    'version': '10.0.1.0.0',
    'category': 'Generic Modules/Projects & Services',
    'author': "Camptocamp,Odoo Community Association (OCA),"
            "Serpent Consulting Services Pvt. Ltd.",
    'license': 'AGPL-3',
    'website': 'https://www.camptocamp.com',
    'depends': ['project',
                'hr_timesheet'],
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
