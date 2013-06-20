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


class DissociateInvoice(orm.TransientModel):
    _name = 'dissociate.aal.to.invoice'
    _description = 'Dissociate Analytic Lines'

    def dissociate_aal(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        aal_obj = self.pool.get('account.analytic.line')
        aal_ids = context.get('active_ids', False)
        if isinstance(ids, list):
            req_id = ids[0]
        else:
            req_id = ids
        ids2 = []
        for id in aal_ids:
            ids2.append(id)
        # Use of SQL here cause otherwise the ORM won't allow to modify the invoiced AAL
        # which is exactly what we want !
        cr.execute("UPDATE account_analytic_line SET invoice_id = NULL WHERE id IN (%s)"%(','.join(map(str, ids2))))

        return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
