/**
 * Kanso document types to export
 */

var Type = require('kanso/types').Type,
    fields = require('kanso/fields'),
    widgets = require('kanso/widgets');

exports.slave = new Type('slave', {
    fields: {
        fqdn: fields.string(),
        last_login: fields.string({required:false}),
        password: fields.string(),
        enabled: fields.boolean(),
        active: fields.boolean()
    },
    allow_extra_fields: true
});

exports.task = new Type('task', {
    fields: {
        name: fields.string(),
        created: fields.createdTime({required:false}),
        started: fields.string({required:false}),
        completed: fields.string({required:false}),
        slave: fields.string({required:false}),
        platform: fields.string({required:false}),
        record_id: fields.string({required: false})
    },
    allow_extra_fields: true
});

exports.record = new Type('record', {
    fields: {
        created: fields.createdTime(),
        title: fields.string(),
        description: fields.string({
            widget: widgets.textarea({cols: 40, rows: 10})
        }),
    },
});

