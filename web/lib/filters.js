/**
 * Filter functions to be exported from the design doc.
 */

exports.record = function(doc, req) {
    if (doc.type == 'record')
        return true;
    else
        return false;
}

