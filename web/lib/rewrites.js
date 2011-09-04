/**
 * Rewrite settings to be exported from the design doc
 */

module.exports = [
    {from: '/static/*', to: 'static/*'},
    {from: '/', to: '_list/index/records_by_created'},
    {from: '/task/:name', to: '_list/task/tasks_by_name', query: {
        // string key must be in list to be properly quoted?
        key: [':name'],
    }},
    {from: '/record/:id', to: '_show/record/:id'},
    {from: '*', to: '_show/not_found'}
];

