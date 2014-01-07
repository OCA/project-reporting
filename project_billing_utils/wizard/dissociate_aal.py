# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Joël Grand-Guillaume, Leonardo Pistone
#    Copyright 2010-2014 Camptocamp SA
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
"""Introduce a wizard to dissociate an Analytic Line from an Invoice."""
from openerp.osv import orm


class DissociateInvoice(orm.TransientModel):

    """Wizard to dissociate an Analytic Line from an Invoice."""

    _name = 'dissociate.aal.to.invoice'
    _description = 'Dissociate Analytic Lines'

    def dissociate_aal(self, cr, uid, ids, context=None):
        """Dissociate invoice from the line and return {}.

        This is necessary because the module hr_timesheet_invoice introduces
        a check that we want to avoid.

        """
        if context is None:
            context = {}

        aal_obj = self.pool.get(context['active_model'])
        ctx = context.copy()
        ctx['skip_invoice_check'] = True
        aal_obj.write(cr, uid, context['active_ids'], {
            'invoice_id': False
        }, ctx)
        return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
