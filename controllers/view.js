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
    res.sendFile("login.html", {root: `${__dirname}/../public/html`});
});
router.get("/login", (req, res) => {
    res.sendFile("login.html", {root: `${__dirname}/../public/html`});
});

//home page
router.get("/home", (req, res) => {
    res.sendFile("home.html", {root: `${__dirname}/../public/html`});
});

//Agent control
router.get("/control", (req, res) => {
    res.sendFile("control.html", {root: `${__dirname}/../public/html`});
});

//Agent creator
router.get("/creator", (req, res) => {
    res.sendFile("creator.html", {root: `${__dirname}/../public/html`});
});

//Button creator
router.get("/button", (req, res) => {
    res.sendFile("button.html", {root: `${__dirname}/../public/html`});
});




module.exports = router;