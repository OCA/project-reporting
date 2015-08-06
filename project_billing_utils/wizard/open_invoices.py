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
from openerp import models, api
from openerp.tools.safe_eval import safe_eval


class OpenInvoicesFromProject(models.TransientModel):
    _name = 'open.invoice.from.project'
    _description = 'Open Invoices'

    @api.multi
    def open_invoices(self):
        aa_obj = self.env['project.project']

        active_ids = self.env.context.get('active_ids', False)
#         aa_rs = self.env['account.analytic.account']
#         for project in aa_obj.browse(active_ids):
#             aa_rs += project.analytic_account_id
        aa_rs = aa_obj.browse(active_ids).mapped('analytic_account_id')

        # Use a SQL request because we can't do that so easily with the ORM
        query = """
            SELECT inv.id from account_invoice inv
                LEFT JOIN account_invoice_line l ON (inv.id=l.invoice_id)
                WHERE l.account_analytic_id IN %s
            """
        self.env.cr.execute(query, (tuple(aa_rs.ids),))

        inv_ids = self.env.cr.fetchall()
        line_ids = []
        for line in inv_ids:
            line_ids.append(line[0])
        inv_type = self.env.context.get('inv_type', 'out_invoice')

        if 'out_invoice' in inv_type:
            xml_id = 'action_invoice_tree1'
        else:
            xml_id = 'action_invoice_tree2'

        result = self.env.ref('account.%s' % xml_id)
        result = result.read()[0]
        invoice_domain = safe_eval(result.get('domain', []))
        invoice_domain.append(('id', 'in', line_ids))
        result['domain'] = invoice_domain
        return result
