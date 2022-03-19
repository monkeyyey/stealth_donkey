const mysql = require("mysql");

var dbconnect = {
    getConnection: function () {
        var conn = mysql.createConnection({
            host: "localhost",
            port: 3306,
            user: "root",
            password: "wobuai88",
            database: "agent",
            // retain date as a string
            dateStrings: true,
        });
        return conn;
    },
};

module.exports = dbconnect;