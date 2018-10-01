##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, api, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo import exceptions

import time


class CreateInvoicesFromProject(models.TransientModel):
    _name = 'create.invoice.from.project'
    _description = 'Create Invoices'

    @api.model
    def _prepare_invoice(self, project):
        """
        Prepare the values used for the invoice creation.
        Override and properly use the `super` chain
        to customize the invoice creation
        """
        if not project.partner_id:
            raise exceptions.Warning(
                _('UserError'),
                _('The Partner is missing on the project:\n%s') % project.name)

        partner = project.partner_id

        date_due = False
        if partner.property_payment_term_id:
            pterm_list = partner.property_payment_term_id.compute(
                value=1,
                date_ref=fields.Date.today())
            if pterm_list:
                pterm_list = [line[0] for line in pterm_list]
                pterm_list.sort()
                date_due = pterm_list[-1]

        return {
            'name': '%s - %s' % (time.strftime('%D'), project.name),
            'type': 'out_invoice',
            'date_due': date_due,
            'partner_id': partner.id,
            'payment_term': partner.property_payment_term_id.id or False,
            'account_id': partner.property_account_receivable_id.id,
            'currency_id': project.currency_id.id,
        }

    @api.multi
    def create_invoices(self):
        assert self.env.context.get('active_ids') is not None, \
            "create_invoices needs active_ids in context"

        project_obj = self.env['project.project']
        invoice_obj = self.env['account.invoice']
        for project in project_obj.browse(self.env.context['active_ids'],):
            values = self._prepare_invoice(project)
            last_invoice = invoice_obj.create(values)
            invoice_obj += last_invoice

        xml_id = 'action_invoice_tree1'
        view = self.env.ref('account.%s' % xml_id)
        result = view.read()[0]
        invoice_domain = safe_eval(result.get('domain', []))
        invoice_domain.append(('id', 'in', invoice_obj.ids))
        result['domain'] = invoice_domain
        return result
