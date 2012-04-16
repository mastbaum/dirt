function(doc) {
  if (doc.type == 'task') {
    emit([doc.name], doc);
  }
}
