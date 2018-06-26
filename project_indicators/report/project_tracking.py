##############################################################################
#
# Copyright (c) 2010 Camptocamp SA
# @author Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

import math
from odoo import models, api


class ProjectTrackingQwebReport(models.AbstractModel):

    _name = 'report.project_indicators.project_tracking'

    @api.multi
    def float_time_convert(self, float_val):
        sign = float_val < 0 and '-' or ''
        hours = math.floor(abs(float_val))
        mins = round(abs(float_val) % 1 + 0.01, 2)
        if mins >= 1.0:
            hours += 1
            mins = 0.0
        else:
            mins *= 60
        float_time = '%s%02d:%02d' % (sign, hours, mins)
        return float_time

    @api.multi
    def total_project_analysis(self, project_id):
        res = {}
        effective_hours = 0.0
        remaining_hours = 0.0
        total_hours = 0.0
        planned_hours = 0.0
        delay_hours = 0.0
        planning_error_percentage = 0.0
        for task in project_id.tasks:
            effective_hours += task.effective_hours
            remaining_hours += task.remaining_hours
            total_hours += task.total_hours
            planned_hours += task.planned_hours
            delay_hours += task.delay_hours
            planning_error_percentage += task.planning_error_percentage
        res.update({'effective_hours': effective_hours,
                    'remaining_hours': remaining_hours,
                    'total_hours': total_hours,
                    'planned_hours': planned_hours,
                    'delay_hours': delay_hours,
                    'planning_error_percentage': planning_error_percentage
                    })
        return [res]

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['project.project'].browse(docids)
        if data is None:
            data = {}
        if not docids:
            docids = data.get('docids')
        return {
            'doc_ids': docids,
            'doc_model': 'project.project',
            'data': data,
            'docs': docs,
            'float_time_convert': self.float_time_convert,
            'total_project': self.total_project_analysis
        }
