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
    return {
        title: doc.title,
        description: doc.description,
        content: templates.render('record.html', req, doc)
    };
};
