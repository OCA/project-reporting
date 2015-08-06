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
from openerp.tools.safe_eval import safe_eval
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
                _('The Partner is missing on the project:\n%s') % project.name)

        if not project.pricelist_id:
            raise osv.except_osv(
                _('UserError'),
                _('The Customer Pricelist is '
                  'missing on the project:\n%s') % project.name)

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

        return {
            'name': '%s - %s' % (time.strftime('%D'), project.name),
            'type': 'out_invoice',
            'date_due': date_due,
            'partner_id': partner.id,
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

        invoices = []
        for project in project_obj.browse(cr, uid, context['active_ids'],
                                          context=context):
            values = self._prepare_invoice(cr, uid, project, context=context)
            last_invoice = invoice_obj.create(cr, uid, values, context=context)
            invoices.append(last_invoice)
        xml_id = 'action_invoice_tree1'
        result = mod_obj.get_object_reference(cr, uid, 'account', xml_id)
        view_id = result and result[1] or False
        result = act_obj.read(cr, uid, view_id, context=context)
        invoice_domain = safe_eval(result['domain'])
        invoice_domain.append(('id', 'in', invoices))
        result['domain'] = invoice_domain
        return result
