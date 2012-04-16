function(doc) {
  if (doc.type == 'record')
    emit([doc._id, 0], doc);
  if (doc.type == 'task')
    emit([doc.record_id, 1], doc);
}
