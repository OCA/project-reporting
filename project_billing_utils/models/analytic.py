##############################################################################
#
#    Author: Leonardo Pistone
#    Copyright 2014 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

"""Changes to allow the dissociate analytic lines wizard to work."""

from odoo import models, api


class AccountAnalyticLine(models.Model):

    """Hack the analytic line to optionally skip the invoice check."""

    _inherit = 'account.analytic.line'

    @api.multi
    def write(self, vals):
        """Put a key in the vals, since we have no context. Return super."""
        if self.env.context.get('skip_invoice_check'):
            vals['_x_vals_skip_invoice_check'] = True
        return super(AccountAnalyticLine, self).write(vals)

    @api.multi
    def _check_inv(self, vals):
        """Optionally skip invoice check. Return boolean."""
        if '_x_vals_skip_invoice_check' in vals:
            del vals['_x_vals_skip_invoice_check']
            return True
        return super(AccountAnalyticLine, self)._check_inv(vals)
