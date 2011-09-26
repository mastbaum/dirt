/**
 * Show functions to be exported from the design doc.
 */

// summary view with basic record information and "percent awesome" bar data
exports.summary = {
    map: function(doc) {
        if (doc.type == 'record')
            emit([doc._id, 1], doc);
        if (doc.type == 'task')
            emit([doc.record_id, 0], doc);
    }
};

// get tasks for a given record
// returns record row followed by associated tasks
exports.tasks_by_record = {
    map: function(doc) {
    if (doc.type == 'record')
        emit([doc._id, 0], doc);
    if (doc.type == 'task')
        emit([doc.record_id, 1], doc);
    }
};

// get a given task for all records
exports.tasks_by_name = {
    map: function(doc) {
        if (doc.type == 'task') {
            emit([doc.name], doc);
        }
    }
};

exports.slaves_by_hostname = {
    map: function(doc) {
        if(doc.type == 'slave')
            emit(doc.fqdn, doc);
    }
};

