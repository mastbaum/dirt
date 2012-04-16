task = function (head, req) {
  var task_name = ''
  var row, rows = [];
  while (row = getRow()) {
    task_name = row.value.name;
    if ('results' in row.value)
      row['results_string'] = JSON.stringify(row.value.results, null, 1)
    var d = new Date();
    d.setTime(1000*row.value.created);
    row.value.created = d.toLocaleString();
    if (row.value.started) {
      d.setTime(1000*row.value.started);
      row.value.started = d.toLocaleString();
    }
    if (row.value.completed) {
      d.setTime(1000*row.value.completed);
      row.value.completed = d.toLocaleString();
    }
    rows.push(row);
  }

  var content = {
    task_name: task_name,
    rows: rows
  };

  return JSON.stringify(content);
};
