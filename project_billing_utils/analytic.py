# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Leonardo Pistone
#    Copyright 2014 Camptocamp SA
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
"""Changes to allow the dissociate analytic lines wizard to work."""

from openerp import models, api


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
