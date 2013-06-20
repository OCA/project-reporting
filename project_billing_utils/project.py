# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Joel Grand-guillaume (Camptocamp)
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class ProjectProject(osv.osv):
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

ProjectProject()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: