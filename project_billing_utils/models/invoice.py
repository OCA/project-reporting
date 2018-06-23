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
