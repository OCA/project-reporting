##############################################################################
#
# Copyright (c) 2010 Camptocamp SA
# @author Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    @api.depends('delay_hours', 'planned_hours')
    def _get_planning_error(self):
        for task in self:
            if task.delay_hours and task.planned_hours:
                task.planning_error_percentage = round(
                    100.0 * task.delay_hours / task.planned_hours, 2)

    planning_error_percentage = fields.Float(
        compute='_get_planning_error', string='Error (%)',
        group_operator="avg",
        help="Computed as: Delay Hours / Planned Hours.")
