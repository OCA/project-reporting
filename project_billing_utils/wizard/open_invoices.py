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


class OpenInvoicesFromProject(osv.osv_memory):
    _name = 'open.invoice.from.project'
    _description = 'Open Invoices'
    

    def open_invoices(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        aa_obj = self.pool.get('project.project')
        
        active_ids = context.get('active_ids', False)
        if isinstance(ids, list):
            req_id = ids[0]
        else:
            req_id = ids
        aa_ids = []
        for project in aa_obj.browse(cr,uid,active_ids):
            aa_ids.append(project.analytic_account_id.id)
        # Use a SQL request because we can't do that so easily with the ORM
        cr.execute("""
        SELECT inv.id from account_invoice inv 
        LEFT JOIN account_invoice_line l ON (inv.id=l.invoice_id) 
        WHERE l.account_analytic_id IN (%s)
        ;""" % (','.join(map(str,aa_ids))))
        
        inv_ids = cr.fetchall()
        line_ids = []
        for line in inv_ids:
            line_ids.append(line[0])
        inv_type = context.get('inv_type','out_invoice')
        
        if inv_type == 'out_invoice':
            xml_id = 'action_invoice_tree1'
        else:
            xml_id = 'action_invoice_tree2'
        result = mod_obj.get_object_reference(cr, uid, 'account', xml_id)
        id = result and result[1] or False
        result = act_obj.read(cr, uid, id, context=context)
        invoice_domain = eval(result['domain'])
        invoice_domain.append(('id', 'in', line_ids))
        result['domain'] = invoice_domain
        return result

OpenInvoicesFromProject()