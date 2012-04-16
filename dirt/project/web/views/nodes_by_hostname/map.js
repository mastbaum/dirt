function(doc) {
  if(doc.type == 'node')
    emit(doc.fqdn, doc);
}
