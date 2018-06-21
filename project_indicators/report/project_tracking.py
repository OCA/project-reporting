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

import time
import math
from openerp import models
from openerp.report import report_sxw


class ReportProjectTracking(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(ReportProjectTracking, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
            'float_time_convert': self.float_time_convert,
            'total_project': self.total_project_analysis
        })

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


class ProjectTrackingQwebReport(models.AbstractModel):
    _name = "report.project_indicators.project_tracking"
    _inherit = "report.abstract_report"
    _template = "project_indicators.project_tracking"
    _wrapped_report_class = ReportProjectTracking
