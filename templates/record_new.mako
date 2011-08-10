# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>Add a new record</h1>

<form action="${request.route_url('record_new')}" method="post">
<table width=90%>
 <tr>
  <td width=5%>Number:</td><td><input type="text" maxlength="100" name="number"></td>
 </tr>
 <tr>
  <td width=5%>UUID:</td><td><input type="text" maxlength="100" name="uuid"></td>
 </tr>
 <tr>
  <td width=5%>Description:</td><td><textarea name="description" cols=40 rows=5></textarea></td>
 </tr>

</table>
  <input type="submit" name="add" value="ADD" class="button">
</form>

