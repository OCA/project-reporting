# Copyright 2020 Jarsa (http://www.jarsa.com.mx)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Project Task Report with Timesheet",
    "summary": "Basic report for project tasks with timesheets.",
    "version": "13.0.1.0.0",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/project-reporting",
    "category": "Project Management",
    "depends": ["project_task_report", "hr_timesheet"],
    "data": ["views/project_task_report.xml", "views/project_task_chatter_report.xml"],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
