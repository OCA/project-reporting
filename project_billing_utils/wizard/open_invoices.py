##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, api
from odoo.tools.safe_eval import safe_eval


class OpenInvoicesFromProject(models.TransientModel):
    _name = 'open.invoice.from.project'
    _description = 'Open Invoices'

    @api.multi
    def open_invoices(self):
        aa_obj = self.env['project.project']

        active_ids = self.env.context.get('active_ids', False)
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
