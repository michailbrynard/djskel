/*global require:true */

require.config({
    baseUrl: "/static/survey/js/",
    paths: {
        "jquery": "../bower_components/jquery/dist/jquery.min",
        "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap.min",
        "select2": "../bower_components/select2/select2.min",
        "jquery-cookie": "../bower_components/jquery-cookie/jquery.cookie",
        "table-dnd": "../bower_components/TableDnD/dist/jquery.tablednd.min",
        //"jquery-placeholder": "../bower_components/jquery-placeholder/jquery.placeholder.min"
    },
    shim: {
        "bootstrap": {
            deps: ["jquery"]
        },
        "select2": {
            deps: ["jquery"]
        },
        "jquery-cookie": {
            deps: ["jquery"]
        },
        //"jquery-placeholder": {
        //    deps: ["jquery"]
        //},
        "table-dnd": {
            deps: ["jquery"]
        }
    },
    packages: []
});

require(["main"]);