# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA
# @author Guewen Baconnier
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


class Project(osv.osv):
    _inherit = "project.project"

    def open_project_indicators(self, cr, uid, ids, context=None):
        ir_model_data_obj = self.pool.get('ir.model.data')
        ir_model_data_id = ir_model_data_obj.search(
            cr, uid, [['model', '=', 'ir.ui.view'],
                      ['name', '=',
                       'account_analytic_account_wizard_indicators']],
            context=context)
        res_id = ir_model_data_obj.read(cr, uid, ir_model_data_id,
                                        fields=['res_id'])[0]['res_id']
        if isinstance(ids, list):
            ids = ids[0]
        project = self.browse(cr, uid, ids, context=context)
        account_id = project.analytic_account_id.id
        return {
            'name': 'Project indicators',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.analytic.account',
            'context': '{}',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'res_id': account_id,
        }


class ProjectTask(osv.osv):
    _inherit = 'project.task'

    def _get_planning_error(self, cr, uid, ids, field_names, args,
                            context=None):
        res = {}.fromkeys(ids, 0.0)
        for task in self.browse(cr, uid, ids, context=context):
            if task.delay_hours and task.planned_hours:
                res[task.id] = round(
                    100.0 * task.delay_hours / task.planned_hours, 2)
        return res

    _columns = {
        'planning_error_percentage': fields.function(
            _get_planning_error, method=True, string='Error (%)', type='float',
            group_operator="avg",
            help="Computed as: Delay Hours / Planned Hours."),
    }
