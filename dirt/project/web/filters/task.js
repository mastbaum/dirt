function(doc, req) {
  if (doc.type == 'task')
    return true;
  else
    return false;
}
