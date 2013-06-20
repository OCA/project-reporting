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
        if context is None:
            context = {}
        ### We will check if the account have no analytic line linked
        if ids and isinstance(ids, int):
            ids = [ids]
        AccountLineobj = self.pool.get('account.analytic.line')
        ProjectObj = self.pool.get('project.project')
        ProjectList = ProjectObj.browse(cr, uid, ids, context=context)
        for project in ProjectList:
            AccountLineIds = AccountLineobj.search(cr, uid, [('account_id', '=', project.analytic_account_id.id)])
            ## If we found line linked with account we raise an error
            if AccountLineIds:
                raise osv.except_osv(_('Invalid Action !'), _('You can\'t delete account %s , analytic lines linked to it' % project.name))
            else:
                super(ProjectProject, self).unlink(cr, uid, [project.id], context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
