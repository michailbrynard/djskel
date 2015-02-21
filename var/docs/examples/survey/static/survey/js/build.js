//noinspection BadExpressionStatementJS
({
    baseUrl: ".",

    paths: {"requireLib": "../bower_components/requirejs/require" },
    //paths: {
    //    "jquery": "../bower_components/jquery/dist/jquery.min",
    //    "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap.min",
    //    "select2": "../bower_components/select2/select2.min",
    //    "jquery-cookie": "../bower_components/jquery-cookie/jquery.cookie",
    //    "table-dnd": "../bower_components/TableDnD/dist/jquery.tablednd.min"
    //},
    name: "main",
    //out: "main-built.js",
    //optimize: 'uglify2',
    //generateSourceMaps: true,
    preserveLicenseComments: false,
    mainConfigFile: 'config.js',

    //name: 'almond.js',
    include: ['main', 'requireLib'],
    insertRequire: ['main'],
    out: 'main-built.js',
    //wrap: true,


    uglify: {
        toplevel: true,
        ascii_only: true,
        //beautify: true,
        max_line_length: 1000,

        //How to pass uglifyjs defined symbols for AST symbol replacement,
        //see "defines" options for ast_mangle in the uglifys docs.
        defines: {
            DEBUG: ['name', 'false']
        }
    }

})

