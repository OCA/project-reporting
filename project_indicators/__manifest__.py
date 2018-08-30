##############################################################################
#
# Copyright (c) 2010 Camptocamp SA
# @author Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################


{
    "name": "Project indicators",
    "version": "11.0.1.0.0",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "category": "Generic Modules/Projects & Services",
    "website": "http://camptocamp.com",
    "license": "AGPL-3",
    "depends": ['sale_timesheet',
                'web'],
    "data": ['views/project_view.xml',
             'views/report.xml',
             'report/project_tracking.xml'],
    "application": False,
    "installable": True,
}
