## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}

        table.project_header { font-size: 11px;
                               border-collapse: collapse; }

        td.time { text-align: center; }

        td.project_title { font-size: 13px;
                           font-weight: bold;
                           text-align: center; }

        tr.last_row td {
             border-bottom:1px solid lightgrey;
        }

        table.tasks { border-collapse: collapse;
                      font-size: 11px; }

        table.tasks tr th { border-bottom: 1px solid lightgrey; }

        table.tasks tr td { border-bottom: 1px solid lightgrey; }
        tr.exceeded { color: red; }
        td.exceeded { font-weight: bold;
                      color: red;}

        tr.totals { border-top: double black; }
        tr.totals td { font-weight: bold; }
    </style>
</head>
<body>
    %for project in objects :
    <% setLang(project.partner_id.lang) %>
    <table width="100%" class="project_header">
        <tr><td colspan="5" class="project_title">${_("Project:")}&nbsp;${ project.name | entity }</td></tr>
        <tr><td colspan="5"/><br/></td></tr>
        <tr><td colspan="5"/><b>${_("Total (with timesheets)")}</b></td></tr>
        <tr>
            <td>${_("Quantity Max")}:</td>
            <td align="right">${ float_time_convert(project.quantity_max) }</td>
            <td>&nbsp;</td>
            <td/>
            <td align="right"/>
        </tr>
        <tr class="last_row">
            <td>${_("Total Time Spent")}:</td>
            <td align="right">${ float_time_convert(project.hours_quantity) }</td>
            <td>&nbsp;</td>
            <td>${_("Remaining Hours")}:</td>
            <td align="right" class="${ project.remaining_hours < 0 and 'exceeded' or ''}">${ float_time_convert(project.remaining_hours) }</td>
        </tr>
        <tr><td colspan="5"/><b>${_("Tasks only")}</b></td></tr>
        <tr>
            <td>${_("Planned Time")}:</td>
            <td align="right">${ float_time_convert(project.planned_hours) }</td>
            <td>&nbsp;</td>
            <td>${_("Total Time")}:</td>
            <td align="right">${ float_time_convert(project.total_hours) }</td>
        </tr>
        <tr>
            <td>${_("Time Spent")}:</td>
            <td align="right">${ float_time_convert(project.effective_hours) }</td>
            <td>&nbsp;</td>
            <td>${_("Difference")}:</td>
            <td align="right">${ float_time_convert(project.total_hours - project.planned_hours) }</td>
        </tr>
        <tr class="last_row">
            <td>${_("Remaining Hours")}</td>
            <td align="right">${ float_time_convert(project.total_hours - project.effective_hours) }</td>
            <td>&nbsp;</td>
            <td>${_("Progress")}:</td>
            <td align="right">${ project.progress_rate or 0 } &#37;</td>
        </tr>
    </table>
    <br />
    <table width="100%" class="tasks">
        <tr>
            <th>${_("Task")}</th>
            <th>${_("Status")}</th>
            <th>${_("Hours Spent")}</th>
            <th>${_("Remaining Hours")}</th>
            <th>${_("Total Hours")}</th>
            <th>${_("Planned Hours")}</th>
            <th>${_("Delay Hours")}</th>
            <th>${_("Error (%)")}</th>
        </tr>
 
        %for task in project.tasks :
        <tr class="${ task.remaining_hours < 0 and 'exceeded' or ''}">
            <td>${ task.name | entity }</td>
            <td>${ task.state | entity }</td>
            <td class="time">${ float_time_convert(task.effective_hours) }</td>
            <td class="time ${ task.remaining_hours < 0 and 'exceeded' or ''}">${ float_time_convert(task.remaining_hours) }</td>
            <td class="time">${ float_time_convert(task.total_hours) }</td>
            <td class="time">${ float_time_convert(task.planned_hours) }</td>
            <td class="time">${ float_time_convert(task.delay_hours) }</td>
            <td class="time">${ task.planning_error_percentage or 0 }</td>
        </tr>
        %endfor

        <tr class="totals">
            <td colspan="2">${_("Totals")}</td>
            <td class="time">${ float_time_convert(project.effective_hours) }</td>
            <td class="time">${ float_time_convert(project.total_hours - project.effective_hours) }</td>
            <td class="time">${ float_time_convert(project.total_hours) }</td>
            <td class="time">${ float_time_convert(project.planned_hours) }</td>
            <td class="time">${ float_time_convert(project.total_hours - project.planned_hours) }</td>
            <td class="time">${ project.planned_hours and round((project.total_hours - project.planned_hours) / project.planned_hours * 100, 2) or 0}</td>
        </tr>

    </table>
    <p style="page-break-after:always"/>
    %endfor
</body>
</html>
