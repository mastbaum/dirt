/**
 * List functions to be exported from the design doc.
 */

var templates = require('kanso/templates');

exports.index = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

    var row, records = {};
    while (row = getRow()) {
        if (row.value.type == 'record') {
            var clip_length = 40;
            var description = row.value.description;
            if (row.value.description.length > clip_length)
                description = description.substring(0, clip_length) + '...';
            records[row.value._id] = {
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

    var content = templates.render('index.html', req, {
        rows: rows
    });

    if (req.client) {
        $('#content').html(content);
        document.title = '%%%{project} :: Overview';
    }
    else {
        return templates.render('base.html', req, {
            content: content,
            title: '%%%{project} :: Overview'
        });
    }
};

exports.record = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

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

    var content = templates.render('record.html', req, {
        name: name,
        description: description,
        pass: pass,
        inprogress: inprogress,
        _id: _id,
        rows: rows
    });

    if (req.client) {
        $('#content').html(content);
        document.title = '%%%{project} :: Overview';
    }
    else {
        return templates.render('base.html', req, {
            content: content,
            title: '%%%{project} :: Overview'
        });
    }
};

exports.task = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

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
    var title = '%%%{project} :: Task Detail: ' + task_name;

    var content = templates.render('task.html', req, {
        task_name: task_name,
        rows: rows
    });

    if (req.client) {
        $('#content').html(content);
        document.title = title;
    }
    else {
        return templates.render('base.html', req, {
            content: content,
            title: title
        });
    }
};

