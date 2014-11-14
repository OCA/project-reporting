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
from openerp.osv import orm, fields


class AssociateInvoice(orm.TransientModel):
    _name = 'associate.aal.to.invoice'
    _description = 'Associate Analytic Lines'
    _columns = {
        'invoice_id': fields.many2one('account.invoice', 'Invoice', required=True),
    }

    def associate_aal(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        aal_obj = self.pool.get(context['active_model'])
        aal_ids = context.get('active_ids', False)
        if isinstance(ids, list):
            req_id = ids[0]
        else:
            req_id = ids
        current = self.browse(cr, uid, req_id, context=context)
        aal_obj.write(cr, uid, aal_ids,
                      {'invoice_id': current.invoice_id.id},
                      context=context)

        return {
            'domain': "[('id','in', [%s])]" % (current.invoice_id.id,),
            'name': 'Associated invoice',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': False,
            'context': context,
            'type': 'ir.actions.act_window',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
