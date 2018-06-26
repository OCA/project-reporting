##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def name_get(self):
        if 'special_search' not in self.env.context:
            return super(AccountInvoice, self).name_get()
        else:
            if not self:
                return []
            # We will return value
            rest = []
            for r in self:
                partner_name = r.partner_id.name_get()
                if partner_name:
                    partner_name = partner_name[0][1]
                rest.append(
                    (r['id'],
                     ('%s - %s - %s' % (r.number or '',
                                        partner_name or '', r.name or ''))
                     )
                    )
                # We will
            return rest

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if 'special_search' not in self.env.context:
            return super(AccountInvoice, self).name_search(
                name, args=args, operator=operator, limit=limit)
        invoices = self.env['account.invoice']
        if not args:
            args = []
        if name:
            invoices = self.search(
                [('number', operator, name)] + args, limit=limit)
        if not invoices:
            invoices = self.search(
                [('commercial_partner_id.name', operator, name)] + args,
                limit=limit)
        if not invoices:
            invoices = self.search(
                [('partner_id.name', operator, name)] + args, limit=limit)
        return invoices.name_get()
