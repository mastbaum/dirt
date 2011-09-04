/**
 * List functions to be exported from the design doc.
 */

var templates = require('kanso/templates');

exports.index = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

    var row, rows = [];
    while (row = getRow()) {
        rows.push(row);
    }

    var content = templates.render('index.html', req, {
        rows: rows
    });

    if (req.client) {
        $('#content').html(content);
        document.title = 'dirt :: Overview';
    }
    else {
        return templates.render('base.html', req, {
            content: content,
            title: 'dirt :: Overview'
        });
    }
};

exports.task = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

    var task_name;
    var row, rows = [];
    while (row = getRow()) {
        task_name = row.value.task.name
        rows.push(row);
    }
    var title = 'dirt :: Task Detail: ' + task_name;

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

