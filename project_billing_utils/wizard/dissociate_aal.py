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
from openerp import models, api


class DissociateInvoice(models.TransientModel):

    """Wizard to dissociate an Analytic Line from an Invoice."""

    _name = 'dissociate.aal.to.invoice'
    _description = 'Dissociate Analytic Lines'

    @api.multi
    def dissociate_aal(self):
        """Dissociate invoice from the line and return {}.

        This is necessary because the module hr_timesheet_invoice introduces
        a check that we want to avoid.

        """
        aal_obj = self.env[self.env.context['active_model']]
        ctx = self.env.context.copy()
        aals = aal_obj.browse(self.env.context['active_ids'])
        ctx['skip_invoice_check'] = True
        aals.with_context(ctx).write({'invoice_id': False})
        return {}
