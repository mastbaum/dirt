/**
 * List functions to be exported from the design doc.
 */

var templates = require('kanso/templates');

exports.index = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

    // fetch all the rows
    var row, rows = [];
    while (row = getRow()) {
        rows.push(row);
    }

    // generate the markup for a list of records
    var content = templates.render('index.html', req, {
        rows: rows
    });

    if (req.client) {
        // being run client-side, update the current page
        $('#content').html(content);
        document.title = 'dirt :: Overview';
    }
    else {
        // being run server-side, return a complete rendered page
        return templates.render('base.html', req, {
            content: content,
            title: 'dirt :: Overview'
        });
    }
};

exports.task = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});
    var task_name = req.query.key.replace(/"/g,'');

    var row, rows = [];
    while (row = getRow()) {
        rows.push(row);
    }

    var content = templates.render('task.html', req, {
        task_name: task_name,
        rows: rows
    });

    if (req.client) {
        $('#content').html(content);
        document.title = 'dirt :: Task Detail';
    }
    else {
        return templates.render('base.html', req, {
            content: content,
            title: 'dirt :: Task Detail'
        });
    }
};

