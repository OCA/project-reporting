#  -*- coding: utf-8 -*-
#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Project task actual report",
    "summary": "Create a report with actual time spent by tasks.",
    "version": "10.0.1.0.0",
    "category": "Project Management",
    "website": "https://github.com/OCA/project-reporting/tree/"
               "10.0/project_task_actual_report",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/project_task_actual_report_views.xml",
    ],
}
