/**
 * Show functions to be exported from the design doc.
 */

var templates = require('kanso/templates');

exports.not_found = function (doc, req) {
    return {
        title: '404 - Not Found',
        content: templates.render('404.html', req, {})
    };
};

exports.record = function (doc, req) {
    // calculate overall success/failure
    var pass = true;
    for (task in doc.tasks) {
        if (!doc.tasks[task]['success']) {
            pass = false;
            break;
        }
    }
    doc['pass'] = pass;

    return {
        title: 'dirt :: Record Detail: ' + doc.title,
        content: templates.render('record.html', req, doc)
    };
};

