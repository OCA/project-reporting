# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Joel Grand-Guillaume. Copyright Camptocamp SA
#
##############################################################################
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################


from osv import fields, osv
from tools.translate import _


class AssociateInvoice(osv.osv_memory):
    _name = 'associate.aal.to.invoice'
    _description = 'Associate Analytic Lines'
    
    _columns = {
        'invoice_id': fields.many2one('account.invoice','Invoice', required=True),
    }

    def associate_aal(self, cr, uid, ids, context):
        aal_obj = self.pool.get('account.analytic.line')
        aal_ids = context.get('active_ids', False)
        if isinstance(ids, list):
            req_id = ids[0]
        else:
            req_id = ids
        current = self.browse(cr, uid, req_id, context)
        aal_obj.write(cr,uid,aal_ids,{"invoice_id":current.invoice_id.id},context)
        
        # view_id = self.pool.get('ir.ui.view').search(cursor, uid, [('name', '=', )])
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

AssociateInvoice()