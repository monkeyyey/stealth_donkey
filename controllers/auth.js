const express = require('express');
const router = express.Router();
const users = require('../Models/login')

router.post('/login', (req, res) => {
    let { username, password } = req.body;
    users.verify(username, password, (err, result) => {
        if (err) return res.status(500).send({ message: 'an error had occurred' });
        if (!result) return res.status(401).send({ message: 'invalid user credentials' });
        res.status(200).send(result)
    })
});

module.exports = router;