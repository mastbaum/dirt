record = function (head, req) {
    var row, rows = [];
    var pass = true;
    var inprogress = false;
    var _id;

    // first row is record
    row = getRow();
    name = row.key[0];
    _id = row.value._id;
    description = row.value.description;

    // subsequent are associated tasks
    while (row = getRow()) {
        if (row.value.kwargs)
            if (row.value.kwargs.testname)
                row.value.name = row.value.kwargs.testname;
        if ('results' in row.value) {
            row['results_string'] = JSON.stringify(row.value.results, null, 1);
            if (!row.value.results.success)
                pass = false;
        }
        if (!row.value.completed)
            inprogress = true;
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
        name: name,
        description: description,
        pass: pass,
        inprogress: inprogress,
        id: _id,
        rows: rows
    };

    return JSON.stringify(content);
};
