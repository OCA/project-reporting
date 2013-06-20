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
from openerp.osv import orm, osv
from openerp.tools.translate import _
import time

class CreateInvoicesFromProject(orm.TransientModel):
    _name = 'create.invoice.from.project'
    _description = 'Create Invoices'

    def create_invoices(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        aa_obj = self.pool.get('project.project')

        active_ids = context.get('active_ids', False)
        if isinstance(ids, list):
            req_id = ids[0]
        else:
            req_id = ids
        aa_ids = []
        invoices = []
        for project in aa_obj.browse(cr, uid, active_ids, context=context):
            partner = project.partner_id
            if (not partner) or not (project.pricelist_id):
                raise osv.except_osv(_('UserError'), _('Please fill in the pricelist and contact fields in the project:\n%s' %(project.name,)))

#            if project.contact_id:
#                inv_contact = project.contact_id.id
#            else:
#                inv_contact = self.pool.get('res.partner').address_get(cr, uid, [project.partner_id.id], adr_pref=['invoice'])['invoice']

            account_payment_term_obj = self.pool.get('account.payment.term')
            date_due=False
            if partner.property_payment_term:
                pterm_list= account_payment_term_obj.compute(cr, uid,
                        partner.property_payment_term.id, value=1,
                        date_ref=time.strftime('%Y-%m-%d'))
                if pterm_list:
                    pterm_list = [line[0] for line in pterm_list]
                    pterm_list.sort()
                    date_due = pterm_list[-1]

            curr_invoice = {
                'name': time.strftime('%D')+' - '+project.name,
                'partner_id': project.partner_id.id,
#                'address_contact_id': self.pool.get('res.partner').address_get(cr, uid, [project.partner_id.id], adr_pref=['contact'])['contact'],
#                'address_invoice_id': inv_contact,
                'payment_term': partner.property_payment_term.id or False,
                'account_id': partner.property_account_receivable.id,
                'currency_id': project.pricelist_id.currency_id.id,
                'type':'out_invoice',
                'date_due': date_due,
            }

            last_invoice = self.pool.get('account.invoice').create(cr, uid, curr_invoice)
            invoices.append(last_invoice)

        xml_id = 'action_invoice_tree1'
        result = mod_obj.get_object_reference(cr, uid, 'account', xml_id)
        id = result and result[1] or False
        result = act_obj.read(cr, uid, id, context=context)
        invoice_domain = eval(result['domain'])
        invoice_domain.append(('id', 'in', invoices))
        result['domain'] = invoice_domain
        return result

CreateInvoicesFromProject()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
