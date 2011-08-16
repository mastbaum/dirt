/**
 * Show functions to be exported from the design doc.
 */
exports.records_by_created = {
    map: function (doc) {
        if (doc.type === 'record') {
            emit(doc.id, {title: doc.title, description: doc.description});
        }
    }
};

exports.tasks_by_name = {
    map: function(doc) {
        if(doc.type == 'record') {
            for(var i in doc.tasks) {
                var task = doc.tasks[i];
                emit(task.name, {'record_id': doc._id, 'record_title': doc.title, 'task': task});
            }
        }
    }
};

