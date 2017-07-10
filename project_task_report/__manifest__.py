# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Task Report",
    "summary": "Basic report for project tasks.",
    "version": "10.0.1.0.0",
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/project-reporting",
    "category": "Project Management",
    "depends": ["project"],
    "data": [
        'views/project_task_report.xml',
        'views/project_task_chatter_report.xml',
    ],
    "license": "AGPL-3",
    'installable': True,
    'application': False,
}
