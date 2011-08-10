# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>All Records</h1>

<div>
 <table width="90%">
  <tr>
   <th>Number</th>
   <th>Comments</th>
   <th># of Tests</th>
   <th>Test Status</th>
  </tr>
  % if records:
   % for record in records:
     <tr>
      <td style="text-align:center;"><a href="${request.route_url('record', record_id=record['id'])}">${record['id']}, ${record['number']}</a>&nbsp;&nbsp;<a href="#"><img src="" border=0></a></td>
      <td width="35%">${record['description']}
      </td>
      <td style="text-align:center;">
      N
      </td>
      <td width="65%">
       <div>
        <span title="Succeeded: %" style="display:inline-block;width:25%;background:green;margin:-3px;">&nbsp;</span>
        <span title="Failed: %" style="display:inline-block;width:25%;background:red;margin:-3px;">&nbsp;</span>
        <span title="In Progress: %" style="display:inline-block;width:25%;background:blue;margin:-3px;">&nbsp;</span>
        <span title="Waiting: %" style="display:inline-block;width:25%;background:gray;margin:-3px;">&nbsp;</span>
       </div>
       <div id=LongDescription_rev${record['number']} style="display:none;margin:10px;padding:6px;">
        long description
       </div>
      </td>
     </tr>
   % endfor
 </table>
 % else:
  <h2>There are no records</h2>
 % endif
</div>

