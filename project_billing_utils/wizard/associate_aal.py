##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, api, fields, _


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
        aal_rs.write({'timesheet_invoice_id': self.invoice_id.id})
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
