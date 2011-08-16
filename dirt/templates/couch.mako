# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>CouchDB Test</h1>
<div>
   % if documents:
    % for doc in documents:
     % for i in doc:
      <h2>${i}</h2>
     % endfor
    % endfor
   % endif
</div>

