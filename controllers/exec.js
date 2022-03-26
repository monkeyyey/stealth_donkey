const express = require('express');
const router = express.Router();

const fs = require('fs');
const { exec } = require('child_process');
const baseUrl = "http://192.168.1.81:5000"


//This will be used for sending files
router.post('/', function(req, res){
    var file_location = req.body.file_location
    const zip = req.body.zip
    file_location = file_location.replace(" ","")
    if (zip == "Yes"){
        exec(`curl ${baseUrl}/file_retrieval_zip > ./retrieval/hi.zip`)  
    }
    else{
        console.log("feefef")
        // exec(`curl -d '{"zip":${zip},"file":${file_location}} -H "Content-Type: application/json" -X POST ${baseUrl}/file_retrieval_2 ' > ./retrieval/sala.txt`)  
        exec(`curl ${baseUrl}/file_retrieval_file?file=${file_location} > ./retrieval/sala.txt`)  
    }
});

module.exports = router;
