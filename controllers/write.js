const fs = require("fs")
var agent = `
import fileinput
import os, shutil, io
from flask import Flask, send_file, request
from flask import Response
from zipfile import ZipFile
from flask_cors import CORS
import platform

# Detect Operating system that Agent is running on
operating_system = platform.system()

# Initialize + Enable Cross origin resource sharing
app = Flask(__name__)
CORS(app)
`
fs.writeFile("./agent.py", agent, (err) => {
    if (err) {
        throw err
    }
})
