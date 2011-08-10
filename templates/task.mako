# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>Task Detail</h1>
<div>
 <table>
  <tr>
   <th>Revision</th>
   <th>Created</th>
   <th>Slave</th>
   <th>Checked Out</th>
   <th>Completed</th>
   <th>Status</th>
   <th>Results</th>
  </tr>
   % if tasks:
    % for task in tasks:
   <tr>
    <td style="text-align:center;"><a href="/record/${task['record_id']}">${task['record_id']}</a>&nbsp;&nbsp;<a href="#"><img src="" border=0></a></td>
    <td style="text-align:center;">${task['created']}</td>
    <td style="text-align:center;">${task['slave_id']}</td>
    <td style="text-align:center;">${task['checked_out']}</td>
    <td style="text-align:center;">${task['completed']}</td>
    <td style="text-align:center;">
     <center>
     % if task['completed']:
      % if task['success']:
       <span title="Succeeded" style="display:block;background:green;width:12px;">&nbsp;</span>
      % else:
       <span title="Failed" style="display:block;background:red;width:12px;">&nbsp;</span>
      % endif
     % else:
      % if task['checked_out']:
      <span title="In Progress" style="display:block;background:blue;width:12px;">&nbsp;</span>
      % else:
       % if task['created']:
        <span title="Waiting" style="display:block;background:gray;width:12px;">&nbsp;</span>
       % else:
        ?
       % endif
      % endif
     % endif
     </center>
    </td>
    <td>
     % if task['completed']:
      % if task['task_type'] == 'rattest':
       <a href="#">Summary</a>, <a href="#">Files</a>
      % endif
     % endif
    </td>
   </tr>
   % endfor
   % endif
  </table>
 </div>
</div>
</div>

