# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math
from xlsxwriter.utility import xl_rowcol_to_cell


try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


class ReportProjectTracking(ReportXlsx):

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

    def generate_xlsx_report(self, workbook, data, projects):
        main_header_format = workbook.add_format({'bold': True,
                                                  'align': 'center',
                                                  'font_name': 'sans-serif',
                                                  'font_size': 14})
        normal_fmt = workbook.add_format({'bold': True,
                                          'align': 'center',
                                          'font_name': 'sans-serif',
                                          'font_size': 10,
                                          'border': 1,
                                          'bg_color': 'silver'})
        normal_fmt2 = workbook.add_format({'font_name': 'sans-serif',
                                           'font_size': 10,
                                           'border': 1})
        row = 0
        col = 0
        worksheet = workbook.add_worksheet("Project Indicatos")
        for project in projects:
            worksheet.set_row(row, 30)
            cell = xl_rowcol_to_cell(row, col)
            cell1 = xl_rowcol_to_cell(row, col + 7)
            rc = cell + ':' + cell1
            worksheet.merge_range(rc, 'Project : ' + project.name,
                                  main_header_format)

            # For Total (With Timesheets) Data
            row += 2
            cell = xl_rowcol_to_cell(row, col)
            cell1 = xl_rowcol_to_cell(row, col + 7)
            rc = cell + ':' + cell1
            worksheet.merge_range(rc, 'Total (With Timesheets)', normal_fmt)
            # Task Summary data
            row += 2
            worksheet.set_row(row, 30)
            worksheet.write(row, col, 'Task', normal_fmt)
            worksheet.write(row, col + 1, 'Status', normal_fmt)
            worksheet.write(row, col + 2, 'Hours \n Spent', normal_fmt)
            worksheet.write(row, col + 3, 'Remaining \n Hours', normal_fmt)
            worksheet.write(row, col + 4, 'Total \n Hours', normal_fmt)
            worksheet.write(row, col + 5, 'Planned \n Hours', normal_fmt)
            worksheet.write(row, col + 6, 'Delay \n Hours', normal_fmt)
            worksheet.write(row, col + 7, 'Error \n (%)', normal_fmt)
            r = row
            for task in project.tasks:
                r += 1
                worksheet.set_row(r, 20)
                worksheet.write(r, col, task.name, normal_fmt2)
                worksheet.write(r, col + 1, task.stage_id.name, normal_fmt2)
                worksheet.write(r, col + 2,
                                self.float_time_convert(task.effective_hours),
                                normal_fmt2)
                remain_hours = task.remaining_hours < 0 and 'exceeded' or ''
                worksheet.write(r, col + 3, remain_hours +
                                self.float_time_convert(task.remaining_hours),
                                normal_fmt2)
                worksheet.write(r, col + 4,
                                self.float_time_convert(task.total_hours),
                                normal_fmt2)
                worksheet.write(r, col + 5,
                                self.float_time_convert(task.planned_hours),
                                normal_fmt2)
                worksheet.write(r, col + 6,
                                self.float_time_convert(task.delay_hours),
                                normal_fmt2)
                worksheet.write(r, col + 7,
                                task.planning_error_percentage or 0,
                                normal_fmt2)
            r = r + 1
            total_cell_no = xl_rowcol_to_cell(r, col)
            total_cell_no1 = xl_rowcol_to_cell(r, col + 1)
            worksheet.merge_range(total_cell_no + ':' + total_cell_no1,
                                  'Totals', normal_fmt)
            effective_hours = sum(
                [task.effective_hours for task in project.tasks])
            total_hours = sum([task.total_hours for task in project.tasks])
            planned_hours = sum([task.planned_hours for task in project.tasks])
            worksheet.write(r, col + 2,
                            self.float_time_convert(effective_hours),
                            normal_fmt2)
            worksheet.write(r, col + 3,
                            self.float_time_convert(
                                total_hours - effective_hours),
                            normal_fmt2)
            worksheet.write(r, col + 4,
                            self.float_time_convert(total_hours),
                            normal_fmt2)
            worksheet.write(r, col + 5,
                            self.float_time_convert(planned_hours),
                            normal_fmt2)
            worksheet.write(r, col + 6,
                            self.float_time_convert(
                                total_hours - planned_hours),
                            normal_fmt2)
            worksheet.write(
                r, col + 7,
                planned_hours and round(
                    (total_hours -
                     planned_hours) /
                    planned_hours * 100, 2) or 0,
                normal_fmt2)
            row = r + 5


ReportProjectTracking('report.project.project.xlsx', 'project.project')
