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
from openerp import models, api, fields, _


class AssociateInvoice(models.TransientModel):
    _name = 'associate.aal.to.invoice'
    _description = 'Associate Analytic Lines'
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 required=True)

    @api.multi
    def associate_aal(self):
        aal_obj = self.env[self.env.context['active_model']]
        aal_ids = self.env.context.get('active_ids', False)
        aal_rs = aal_obj.browse(aal_ids)
        aal_rs.write({'invoice_id': self.invoice_id.id})
        return {
            'domain': "[('id','in', [%s])]" % (self.invoice_id.id,),
            'name': _('Associated invoice'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': False,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
        }
