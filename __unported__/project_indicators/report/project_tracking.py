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

from report import report_sxw


class report_project_tracking(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_project_tracking, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
            'float_time_convert': self.float_time_convert,
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


report_sxw.report_sxw('report.project.tracking',
                      'project.project',
                      'addons/project_indicators/report/project_tracking.mako',
                      parser=report_project_tracking)
