/**
 * Kanso document types to export
 */

var Type = require('kanso/types').Type,
    fields = require('kanso/fields'),
    widgets = require('kanso/widgets');

exports.slave = new Type('slave', {
    fields: {
        hostname: fields.string(),
        last_login: fields.string({required:false}),
        password: fields.string(),
        enabled: fields.boolean()
    }
});

exports.task = new Type('task', {
    fields: {
        name: fields.string(),
        created: fields.createdTime({required:false}),
        slave_id: fields.string({required:false}),
        checked_out: fields.string({required:false}),
        completed: fields.string({required:false}),
        success: fields.boolean({required:false}),
        results: fields.string({required:false}),
        task_type: fields.string(),
        platform: fields.string()
    }
});

exports.record = new Type('record', {
    fields: {
        created: fields.createdTime(),
        title: fields.string(),
        description: fields.string({
            widget: widgets.textarea({cols: 40, rows: 10})
        }),
        tasks: fields.embedList({
            type: exports.task,
            required: 'false'
        }),
    }
});

