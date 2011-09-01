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
import time

class CreateInvoicesFromProject(osv.osv_memory):
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
        for project in aa_obj.browse(cr,uid,active_ids):
            partner = project.partner_id
            if (not partner) or not (project.pricelist_id):
                raise osv.except_osv(_('UserError'), _('Please fill in the pricelist and contact fields in the project:\n%s' %(project.name,)))
            if project.contact_id:
                inv_contact=project.contact_id.id
            else:
                inv_contact=self.pool.get('res.partner').address_get(cr, uid, [project.partner_id.id], adr_pref=['invoice'])['invoice']
            
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
                'address_contact_id': self.pool.get('res.partner').address_get(cr, uid, [project.partner_id.id], adr_pref=['contact'])['contact'],
                'address_invoice_id': inv_contact,
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