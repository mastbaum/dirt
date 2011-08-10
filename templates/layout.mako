# -*- coding: utf-8 -*- 
<!DOCTYPE html>  
<head>	
 <meta charset="utf-8">
 <title>Pyramid Task's List Tutorial</title>
 <meta name="author" content="Pylons Project">
 <link rel="shortcut icon" href="/static/favicon.ico">
 <link rel="stylesheet" href="/static/style.css">
</head>

<body class="dashboard">

 % if request.session.peek_flash():
  <div id="flash">
   <% flash = request.session.pop_flash() %>
    % for message in flash:
     ${message}<br>
    % endfor
  </div>
 % endif

 <div id="header">
  <a href="/">
  <div id="branding">
   <h1 id="site-name">Title!</h1>
  </div>
  </a>
 </div>

 <div id="content" class="colMS" style="width:80%;">
  <div id="content-main">
   ${next.body()}
  </div>
 </div>

 <div>
  <h3>Legend</h3>
  <table>
   <tr>
    <td><span style="display:block;background:green;width:12px;">&nbsp;</span></td>
    <td>Succeeded</td>
   </tr>
   <tr>
    <td><span style="display:block;background:red;width:12px;">&nbsp;</span></td>
    <td>Failed</td>
   </tr>
   <tr>
    <td><span style="display:block;background:blue;width:12px;">&nbsp;</span></td>
    <td>In Progress</td>
   </tr>
   <tr>
    <td><span style="display:block;background:gray;width:12px;">&nbsp;</span></td>
    <td>Waiting</td>
   </tr>
  </table>
 </div>
 
</body>
</html>

