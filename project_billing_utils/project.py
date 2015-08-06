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
from openerp import models, api, _
from openerp import exceptions


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
                raise exceptions.Warning(
                    _('Invalid Action'),
                    _('You cannot delete account %s as there are analytic '
                      'lines linked to it') % project.name)
            else:
                super(ProjectProject, project).unlink()
        return True
