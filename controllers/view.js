const express = require('express');
const router = express.Router();
var bodyParser = require('body-parser');
var cors = require('cors');
var urlencodedParser = bodyParser.urlencoded({ extended: false });

router.options('*', cors());
router.use(cors());
router.use(bodyParser.json());
router.use(urlencodedParser);

//login page
router.get("/", (req, res) => {
    console.log('html here')
    res.sendFile("home.html", {root: `${__dirname}/../public/html`});
});
router.get("/login", (req, res) => {
    res.sendFile("login.html", {root: `${__dirname}/../public/html`});
});

//home page
router.get("/home", (req, res) => {
    res.sendFile("home.html", {root: `${__dirname}/../public/html`});
});

module.exports = router;