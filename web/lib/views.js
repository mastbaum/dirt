/**
 * Show functions to be exported from the design doc.
 */
exports.records_by_created = {
    map: function (doc) {
        if (doc.type == 'record') {
            var percents = {'failed': 0, 'success': 0, 'inprogress': 0, 'waiting': 0};
            for (tasknum in doc.tasks) {
                task = doc.tasks[tasknum];
                if (task.completed) {
                    if (task.success)
                        percents['success'] += 1;
                    else
                        percents['failed'] += 1;
                }
                else {
                    if (task.checked_out)
                        percents['inprogress'] += 1;
                    else
                        percents['waiting'] += 1;
                }
            }
            for (item in percents)
                percents[item] = percents[item] * 100 / doc.tasks.length;
            emit(doc._id, {title: doc.title, description: doc.description, task_count: doc.tasks.length, percents: percents});
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

