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

class OpenInvoicesFromProject(orm.TransientModel):
    _name = 'open.invoice.from.project'
    _description = 'Open Invoices'

    def open_invoices(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        aa_obj = self.pool.get('project.project')

        active_ids = context.get('active_ids', False)
        print str(active_ids)
        if isinstance(ids, list):
            req_id = ids[0]
        else:
            req_id = ids
        aa_ids = []
        for project in aa_obj.browse(cr, uid, active_ids):
            aa_ids.append(project.analytic_account_id.id)
        # Use a SQL request because we can't do that so easily with the ORM
        cr.execute("""
        SELECT inv.id from account_invoice inv
        LEFT JOIN account_invoice_line l ON (inv.id=l.invoice_id)
        WHERE l.account_analytic_id IN (%s)
        ;""" % (','.join(map(str, aa_ids))))

        inv_ids = cr.fetchall()
        line_ids = []
        for line in inv_ids:
            line_ids.append(line[0])
        inv_type = context.get('inv_type', 'out_invoice')

        if 'out_invoice' in inv_type:
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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
