const express = require("express");
const app = express();

// Importing cors for cross origin resource sharing
const cors = require("cors");
app.use(cors());

// Content parsing
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Static content
app.use('/css', express.static('./public/css'));
app.use('/js', express.static('./public/js'));
app.use('/img', express.static('./public/images'));

// Controller for serving web pages
app.use(require('./controllers/view'));

// Map api
app.use('/api/file', require('./controllers/send_file'))
app.use('/api/auth', require('./controllers/auth'))

module.exports = app;