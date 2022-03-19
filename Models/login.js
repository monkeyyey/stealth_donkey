const db = require('./DatabaseConfig');

module.exports = {
    verify: function (username, password, callback) {
        let conn = db.getConnection();
        conn.connect((err) => {
            if (err) return callback(err, null);
    
            let sql = `SELECT id, username, admin FROM users WHERE username = ? and password=?`;
            conn.query(sql, [username, password], (err, results) => {
                conn.end();
                if (err) return callback(err, null);
                if (results.length < 1) return callback(null, null);
                else {
                    const user = results[0]
                    return callback(null, user)
                }
            });
        });
    }
}
