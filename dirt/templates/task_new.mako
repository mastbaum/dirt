# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>Add a new record</h1>

<form action="${request.route_url('task_new')}" method="post">
<table width=90%>
 <tr>
  <td width=5%>Name:</td><td><input type="text" maxlength="100" name="name"></td>
 </tr>
 <tr>
  <td width=5%>Record ID:</td><td><input type="text" maxlength="100" name="record_id"></td>
 </tr>
 <tr>
  <td width=5%>Created:</td><td><input type="text" maxlength="100" name="created"></td>
 </tr>
 <tr>
  <td width=5%>Slave ID:</td><td><input type="text" maxlength="100" name="slave_id"></td>
 </tr>
 <tr>
  <td width=5%>Checked out:</td><td><input type="text" maxlength="100" name="checked_out"></td>
 </tr>
 <tr>
  <td width=5%>Completed:</td><td><input type="text" maxlength="100" name="completed"></td>
 </tr>
 <tr>
  <td width=5%>Success:</td><td><input type="text" maxlength="100" name="success"></td>
 </tr>
 <tr>
  <td width=5%>Results:</td><td><input type="text" maxlength="100" name="results"></td>
 </tr>
 <tr>
  <td width=5%>Task type:</td><td><input type="text" maxlength="100" name="task_type"></td>
 </tr>
 <tr>
  <td width=5%>Platform:</td><td><input type="text" maxlength="100" name="platform"></td>
 </tr>
</table>
  <input type="submit" name="add" value="ADD" class="button">
</form>

