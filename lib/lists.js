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
        document.title = 'MyThinger';
    }
    else {
        // being run server-side, return a complete rendered page
        return templates.render('base.html', req, {
            content: content,
            title: 'MyAwesomeThinger'
        });
    }
};

exports.task = function (head, req) {
    start({code: 200, headers: {'Content-Type': 'text/html'}});

    var row, rows = [];
    while (row = getRow()) {
        rows.push(row);
    }

    var content = templates.render('task.html', req, {
        rows: rows
    });

    if (req.client) {
        $('#content').html(content);
        document.title = 'MyThinger';
    }
    else {
        return templates.render('base.html', req, {
            content: content,
            title: 'MyAwesomeThinger'
        });
    }
};

