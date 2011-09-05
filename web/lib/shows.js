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
    var inprogress = false;
    for (task in doc.tasks) {
        doc.tasks[task]['results_string'] = JSON.stringify(doc.tasks[task]['results'], null, 1)
        if (!doc.tasks[task]['results']['success']) {
            pass = false;
        }
        if (!doc.tasks[task]['completed']) {
            inprogress = true;
        }
    }
    doc['pass'] = pass;
    doc['inprogress'] = inprogress;
    return {
        title: 'dirt :: Record Detail: ' + doc.title,
        content: templates.render('record.html', req, doc)
    };
};

