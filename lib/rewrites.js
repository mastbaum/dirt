/**
 * Rewrite settings to be exported from the design doc
 */

module.exports = [
    {from: '/static/*', to: 'static/*'},
    {from: '/', to: '_list/index/records_by_created'},
    {from: '/task/:name', to: '_list/task/tasks_by_name'},
    {from: '/record/:id', to: '_show/record/:id'},
    {from: '*', to: '_show/not_found'}
];

