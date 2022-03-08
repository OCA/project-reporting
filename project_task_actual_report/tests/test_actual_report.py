#  -*- coding: utf-8 -*-
#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo.fields import Datetime
from odoo.tests import SavepointCase


class TestActualReport(SavepointCase):

    def setUp(self):
        super(TestActualReport, self).setUp()
        self.report_model = self.env['project.task.actual.report']
        task_model = self.env['project.task']
        task_id = task_model.name_create("Test actual report")[0]
        self.task = task_model.browse(task_id)

    def test_progress_time(self):
        """
        Let a task be in progress for one hour.

        Check that the report shows
        that such task has been in progress for one hour.
        """
        now = Datetime.from_string(Datetime.now())
        in_progress_time = timedelta(hours=1)
        creation_date = now
        blocked_date = now + in_progress_time

        # Simulate that task has been created 1 hour ago
        creation_message = self.task.message_ids
        self.assertTrue(len(creation_message), 1)
        self.assertTrue(self.task.kanban_state, 'normal')
        creation_message.date = creation_date

        # Simulate that task is `now` blocked
        self.task.kanban_state = 'blocked'
        blocked_message = self.task.message_ids.filtered(
            lambda m: m != creation_message
        )
        self.assertEqual(len(blocked_message), 1)
        blocked_message.date = blocked_date

        # Check that the task has been blocked for 1 hour
        self.assertEqual(
            Datetime.from_string(blocked_message.date)
            - Datetime.from_string(creation_message.date),
            in_progress_time)

        # Find the lines for blocked task
        actual_report_lines = self.report_model.search([
            ('task_id', '=', self.task.id),
        ])
        self.assertEqual(len(actual_report_lines), 2)

        # Check that there is one line representing the 1-hour progress
        kanban_states = dict(
            self.task._fields['kanban_state']
                ._description_selection(self.env)
        )
        report_line = actual_report_lines.filtered(
            lambda rl: rl.kanban_state == kanban_states['normal']
        )
        self.assertEqual(len(report_line), 1)
        self.assertAlmostEqual(report_line.duration, 1, places=3)
