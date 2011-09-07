/**
 * Filter functions to be exported from the design doc.
 */

// used for changes feed
exports.task = function(doc, req) {
    if (doc.type == 'task')
        return true;
    else
        return false;
}

