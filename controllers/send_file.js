const express = require('express');
const router = express.Router();
const archiver = require('archiver');
const fs = require('fs');
const { exec } = require('child_process');


//This will be used for sending files
router.get('/get_File', function(req, res){
    file_name = "databack.txt"
    res.download(`./Exports/${file_name}`, function(error){
        if (error){
            console.log("Error: ", error)
        }

    });
});

//This will be used for sending folders
router.get('/get_Zip', function(req, res){
    directory = "./Exports/zippyman"
    output = "./Exports/compressed2.zip"
    // exec(`7z a ${output} ${directory}`)
    exec("7z a Exports/zippyman ./Exports/compressed2.zip")
    res.download(`${output}`, function(error){
        if (error){
            console.log("Error: ", error)
        }
        //exec(`del ${output}`)
    });
});

//to zip folders
function zipDirectory(sourceDir, outPath) {
    const archive = archiver('zip', { zlib: { level: 9 }});
    const stream = fs.createWriteStream(outPath);

    return new Promise((resolve, reject) => {
    archive
        .directory(sourceDir, false)
        .on('error', err => reject(err))
        .pipe(stream)
    ;

    stream.on('close', () => resolve());
    archive.finalize();
    });
}

module.exports = router;