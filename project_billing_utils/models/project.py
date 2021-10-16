##############################################################################
#
#    Author: Joël Grand-Guillaume
#    Copyright 2010 Camptocamp SA
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, api, _
from odoo.exceptions import UserError


class ProjectProject(models.Model):
    _inherit = 'project.project'
    _description = 'Project'

    @api.multi
    def unlink(self):
        # We will check if the account have no analytic line linked
        account_line_obj = self.env['account.analytic.line']
        for project in self:
            account_lines = account_line_obj.search(
                [('account_id', '=', project.analytic_account_id.id)])
            # If we found line linked with account we raise an error
            if account_lines:
                raise UserError(
                    _('You cannot delete project %s as there are analytic '
                      'lines linked to it') % project.name)
            else:
                super(ProjectProject, project).unlink()
        return True
