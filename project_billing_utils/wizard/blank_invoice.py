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

from openerp.osv import osv, orm
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
import time


class CreateInvoicesFromProject(orm.TransientModel):
    _name = 'create.invoice.from.project'
    _description = 'Create Invoices'

    def _prepare_invoice(self, cr, uid, project, context=None):
        """
        Prepare the values used for the invoice creation.
        Override and properly use the `super` chain
        to customize the invoice creation
        """
        if not project.partner_id:
            raise osv.except_osv(
                    _('UserError'),
                    _('The Partner is missing on the project:\n%s' % project.name))

        if not project.pricelist_id:
            raise osv.except_osv(
                    _('UserError'),
                    _('The Customer Pricelist is '
                      'missing on the project:\n%s' % project.name))

        partner_obj = self.pool.get('res.partner')
        account_payment_term_obj = self.pool.get('account.payment.term')

        partner = project.partner_id

        date_due = False
        if partner.property_payment_term:
            pterm_list = account_payment_term_obj.compute(
                    cr, uid,
                    partner.property_payment_term.id,
                    value=1,
                    date_ref=time.strftime('%Y-%m-%d'),
                    context=context)
            if pterm_list:
                pterm_list = [line[0] for line in pterm_list]
                pterm_list.sort()
                date_due = pterm_list[-1]

        if project.contact_id:
            inv_contact = project.contact_id.id
        else:
            inv_contact = partner_obj.address_get(
                    cr, uid,
                    [partner.id],
                    adr_pref=['invoice'])['invoice']

        return {
            'name': '%s - %s' % (time.strftime('%D'), project.name),
            'type':'out_invoice',
            'date_due': date_due,
            'partner_id': partner.id,
            'address_contact_id': partner_obj.address_get(
                    cr, uid,
                    [partner.id],
                    adr_pref=['contact'])['contact'],
            'address_invoice_id': inv_contact,
            'payment_term': partner.property_payment_term.id or False,
            'account_id': partner.property_account_receivable.id,
            'currency_id': project.pricelist_id.currency_id.id,
        }

    def create_invoices(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        assert context.get('active_ids') is not None, \
            "create_invoices needs active_ids in context"

        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        project_obj = self.pool.get('project.project')
        invoice_obj = self.pool.get('account.invoice')

        aa_ids = []
        invoices = []
        for project in project_obj.browse(cr, uid, context['active_ids'], context=context):
            values = self._prepare_invoice(cr, uid, project, context=context)
            last_invoice = invoice_obj.create(cr, uid, values, context=context)
            invoices.append(last_invoice)

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        view_id = result and result[1] or False
        result = act_obj.read(cr, uid, view_id, context=context)
        invoice_domain = eval(result['domain'])
        invoice_domain.append(('id', 'in', invoices))
        result['domain'] = invoice_domain
        return result

