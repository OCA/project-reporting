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


class ProjectProject(orm.Model):
    _inherit = 'project.project'
    _description = 'Project'

    def unlink(self, cr, uid, ids, context=None):
        # We will check if the account have no analytic line linked
        if ids and isinstance(ids, (int, long)):
            ids = [ids]
        account_line_obj = self.pool['account.analytic.line']
        project_list = self.browse(cr, uid, ids, context=context)
        for project in project_list:
            account_line_ids = account_line_obj.search(
                cr, uid, [('account_id', '=', project.analytic_account_id.id)],
                context=context)
            # If we found line linked with account we raise an error
            if account_line_ids:
                raise osv.except_osv(
                    _('Invalid Action !'),
                    _('You can\'t delete account %s , analytic lines linked '
                      'to it' % project.name))
            else:
                super(ProjectProject, self).unlink(
                    cr, uid, [project.id], context=context)
        return True
