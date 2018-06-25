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
