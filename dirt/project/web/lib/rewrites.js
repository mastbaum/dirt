/**
 * Rewrite settings to be exported from the design doc
 */

module.exports = [
    {from: '/static/*', to: 'static/*'},
    {from: '/', to: '_list/index/summary', query: {
        descending: 'true'
    }},
    {from: '/task/:name', to: '_list/task/tasks_by_name', query: {
        // string key must be in list to be properly quoted?
        startkey: [':name', {}],
        endkey: [':name'],
        descending: 'true'
    }},
    {from: '/record/:id', to: '_list/record/tasks_by_record', query: {
        startkey: [':id'],
        endkey: [':id', 2]
    }},
    {from: '*', to: '_show/not_found'}
];

