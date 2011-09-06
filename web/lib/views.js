/**
 * Show functions to be exported from the design doc.
 */

// summary view with basic record information and "percent awesome" bar data
exports.summary = {
    map: function(doc) {
        if (doc.type == "record")
            emit([doc._id, 0], doc);
        else if (doc.type == "task")
            emit([doc.record_id, 1], doc)
    },
    // must use group_level 1 for meaningful output
    reduce: function(keys, values) {
        var ntasks = 0
        output = {name: '', description: '', task_coumt: 0, percents: {success: 0, failed: 0, waiting: 0, inprogress: 0}};
        for (idx in values) {
            if (values[idx].type == "record")
                if(!output.name) {
                    output.name = values[idx].title;
                    output.description = values[idx].description;
                }
            if (values[idx].type == "task") {
                ntasks += 1;
                if (values[idx].completed) {
                    if (values[idx].results.success)
                        output.percents.success += 1;
                    else
                        output.percents.failed += 1;
                } else {
                    if (values[idx].checked_out)
                        output.percents.inprogress += 1;
                    else
                        output.percents.waiting += 1;
                }
            }
        }
        output.task_count = ntasks;
        for (item in output.percents)
            output.percents[item] = output.percents[item] * 100 / ntasks;
        return output;
    }
};

// get tasks for a given record
exports.tasks_by_record = {
    map: function(doc) {
        if (doc.type == 'record')
            emit([doc._id, 0], doc);
        if (doc.type == 'task') {
            emit([doc.record_id, 1], doc);
        }
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

