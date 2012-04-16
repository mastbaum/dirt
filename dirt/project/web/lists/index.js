function (head, req) {
  var row, records = {};

  while (row = getRow()) {
    if (row.value.type == 'record') {
      var clip_length = 40;
      var description = row.value.description;
      if (row.value.description.length > clip_length)
        description = description.substring(0, clip_length) + '...';
      records[row.value._id] = {
        id: row.value._id,
        changeset_url: row.value.changeset_url,
        success: true,
        name: row.key[0],
        description: description,
        ntasks: 0,
        pass: 0,
        fail: 0,
        inprogress: 0,
        waiting: 0
      };
    }
    else {
      var r_id = row.value.record_id;
      records[r_id].ntasks += 1;
      if (row.value.completed) {
        if (row.value.results.success)
          records[r_id].pass += 1;
        else {
          records[r_id].fail += 1;
          records[r_id].success = false;
        }
      } else {
        if (row.value.started)
          records[r_id].inprogress += 1;
        else
          records[r_id].waiting += 1;
      }
    }
  }

  var rows = [];
  for (r_id in records) {
    records[r_id].pass = records[r_id].pass * 100 / records[r_id].ntasks;
    records[r_id].fail = records[r_id].fail * 100 / records[r_id].ntasks;
    records[r_id].inprogress = records[r_id].inprogress * 100 / records[r_id].ntasks;
    records[r_id].waiting = records[r_id].waiting * 100 / records[r_id].ntasks;
    rows.push(records[r_id]);
  }

  return JSON.stringify(rows);
};
