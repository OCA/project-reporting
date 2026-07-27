# Copyright 2020 Jarsa (http://www.jarsa.com.mx)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProjectTaskTimesheetReport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {"name": "Test Project", "allow_timesheets": True}
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": cls.project.id,
                "allocated_hours": 10.0,
                "description": "Task description",
            }
        )
        cls.employee = cls.env["hr.employee"].create({"name": "Test Employee"})
        cls.env["account.analytic.line"].create(
            {
                "name": "Work done",
                "project_id": cls.project.id,
                "task_id": cls.task.id,
                "employee_id": cls.employee.id,
                "unit_amount": 2.0,
            }
        )

    def _render_report(self, report_ref):
        html = self.env["ir.actions.report"]._render_qweb_html(
            report_ref, self.task.ids
        )[0]
        return html.decode()

    def test_task_report_includes_timesheets(self):
        html = self._render_report("project_task_report.report_project_task_action")
        self.assertIn("Timesheets", html)
        self.assertIn("Work done", html)
        self.assertIn("Test Employee", html)
        self.assertIn("Planned Hours", html)
        self.assertIn("Effective Hours", html)
        self.assertIn("Remaining Hours", html)

    def test_task_chatter_report_includes_timesheets(self):
        html = self._render_report(
            "project_task_report.report_project_task_chatter_action"
        )
        self.assertIn("Timesheets", html)
        self.assertIn("Work done", html)
