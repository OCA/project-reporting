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
from openerp.osv import orm


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if 'special_search' not in context:
            return super(AccountInvoice, self).name_get(
                cr, uid, ids, context=context)
        else:
            if not ids:
                return []
            # We will return value
            rest = []
            for r in self.read(cr, uid, ids, ['number', 'partner_id', 'name'],
                               context=context):
                rest.append(
                    (r['id'],
                     ('%s - %s - %s' % (r['number'] or '',
                                        r['partner_id'][1], r['name'] or ''))))
                # We will
            return rest

    def name_search(self, cr, user, name, args=None, operator='ilike',
                    context=None, limit=100):
        if context is None:
            context = {}
        if 'special_search' not in context:
            return super(AccountInvoice, self).name_search(
                cr, user, name, args=args, operator=operator, context=context,
                limit=limit)
        ids = []
        if not args:
            args = []
        if name:
            ids = self.search(
                cr, user, [('number', operator, name)] + args, limit=limit,
                context=context)
        if not ids:
            ids = self.search(
                cr, user,
                [('commercial_partner_id.name', operator, name)] + args,
                limit=limit, context=context)
        if not ids:
            ids = self.search(
                cr, user,
                [('partner_id.name', operator, name)] + args, limit=limit,
                context=context)
        return self.name_get(cr, user, ids, context=context)
