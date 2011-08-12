# -*- coding: utf-8 -*- 
##############################################################################
#
# @author J Grand-Guillaume
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
{
    "name" : "Analytic and project wizard for services companies",
    "description" : """
Improve the view of analytic and timesheet lines for the project manager
Add wizard to manage project and invoicing :
 - Associate Analytic Lines to invoice (from an invoice or from analytic line directly)
 - Dissociate Analytic Lines from an invoice
 - Get all invoice from Project (with recurssion in child account)
 - Get Analytic Lines from project (with recurssion in child account)
 - Get Analytic Lines from an invoice for controlling
 
    """,
    "version" : "1.4",
    "author" : "Camptocamp",
    "category" : "Generic Modules/Projects & Services",
    "website": "http://www.camptocamp.com",
    "depends" : ["project", "hr_timesheet_invoice"],
    "init_xml" : [],
    "update_xml" : [
            "invoice_view.xml",
            "project_view.xml",
            "wizard/associate_aal_view.xml",
            "wizard/dissociate_aal_view.xml",
            "wizard/open_invoices_view.xml",
    ],
    "active": False,
    "installable": True
}
