##############################################################################
#
#    Author: Joël Grand-Guillaume, Leonardo Pistone
#    Copyright 2010-2014 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

"""Introduce a wizard to dissociate an Analytic Line from an Invoice."""
from odoo import models, api


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
        aals.with_context(ctx).write({'timesheet_invoice_id': False})
        return {}
