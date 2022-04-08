
import fileinput
import os, shutil, io
from flask import Flask, send_file, request
from flask import Response
from zipfile import ZipFile
from flask_cors import CORS
import platform
import json

# Detect Operating system that Agent is running on
operating_system = platform.system()

# Admin URL
admin_url = "https://192.168.1.81:8080"

# Initialize + Enable Cross origin resource sharing
app = Flask(__name__)
CORS(app)
    
#1. get file/zip file from server (URL example: http://127.0.0.1:5000/getfile?type=file)
@app.route("/getfile")
def getFile():
    
    # Retrieve URL params
    type = request.args.get('type')

    # Get file/zip file using curl
    if type == "file":
        os.system(f'curl --insecure {admin_url}/api/file/get_File > databack.txt')
        return Response(status=201)
    elif type == "zip":
        os.system(f'curl --insecure {admin_url}/api/file/get_Zip > compressed2.zip')
        return Response(status=201)

    # file type in params invalid
    return Response(status=400)
        
        
#2. Command Execution + output to file
@app.route("/command", methods = ['POST'])
def command():

    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    command = request_data['cmd']
    exec_only = request_data['exec_only']
    output_destination = request_data['command_output']

    # Execute only
    if exec_only == 'Yes':
        os.system(f'{command}')
    
    # Execute + save result
    else:
        os.system(f'{command} > {output_destination}')

    return Response(status=201)
        
        
#3. Collection of specific files + copy to specific folder
@app.route("/file_collection", methods = ['POST'])
def file_collection():

    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    output_destination = request_data['output']
    collect = request_data['collect']
    files = request_data['files']

    # Splitting the file input to check length + strip blank space
    files = list(map(str.strip, files.split(',')))

    # copy files to outout destination
    if operating_system == 'Windows':
        for file in files:
            file2 = file.split('\\')[-1]
            os.system(f'copy {file} {output_destination}{file2}')
    else:
        for file in files:
            file2 = file.split('/')[-1]
            os.system(f'cp {file} ./{output_destination}/{file2}')
    
    # zip files in output destination
    shutil.make_archive('collection', 'zip', f'{output_destination}')
    if collect == "Yes":
        if operating_system == "Windows":
            return send_file(f'collection.zip')
        else:
            return send_file(f'./collection.zip')
    
    return Response(status=201)
        
        
#4. Send files to another server via SSH
@app.route("/ssh_send", methods = ['POST'])
def ssh_send():


    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    ssh_ip = request_data['ssh_ip']
    ssh_user = request_data['ssh_user']
    ssh_pass = request_data['ssh_pass']
    ssh_files = request_data['ssh_files']
    ssh_output = request_data['ssh_output']

    # Setting commands based on operating system
    if operating_system == 'Windows':
        copy = 'copy'
        delete = 'del /f'
    else:
        copy = 'cp'
        delete = 'rm'

    # Copy each specified file into the 'send_ssh' folder
    for file in ssh_files.split(','):
        file = file.strip()
        file2 = file.split('/')[-1]
        os.system(f'{copy} {file} ./send_ssh/{file2}')

    # zipping the 'send_ssh' folder to 'send_ssh.zip'
    shutil.make_archive(f'send_ssh', 'zip', 'send_ssh')

    # using SCP to send the zip file to the server
    os.system(f'sshpass -p "{ssh_pass}" scp send_ssh.zip {ssh_user}@{ssh_ip}:{ssh_output}')

    # delete the zip file after sending to the ssh_server
    os.system(f'{delete} send_ssh.zip')

    # Emptying the 'send_ssh' folder after sending to avoid cluttering
    if operating_system == 'Windows':
        os.system(f'del /S /q send_ssh')
    else:
        os.system(f'rm -r send_ssh/*')
        
    return Response(status=201)
            
        
#5. Retrieve specific file(s) from client
@app.route("/file_retrieval", methods = ['POST'])
def file_retrieval():
                                                    
    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    file_location = request_data['file_location']

    # Splitting the file input to check length + strip blank space
    file_location = list(map(str.strip, file_location.split(',')))

    # copy files to 'retrieval folder'
    if len(file_location) != 1:
        if operating_system == 'Windows':
            for file in file_location:
                file2 = file.split('\\')[-1]
                os.system(f'copy {file} retrieval{file2}')
        else:
            for file in file_location:
                file2 = file.split('/')[-1]
                os.system(f'cp {file} ./retrieval/{file2}')

    return Response(status=201)

#6. Retrieve file from endpoint 7
@app.route("/file_retrieval_file", methods = ['GET'])
def file_retrieval_file():
    file = request.args.get("file")
    return send_file(file)

#7. Retrieve zip from endpoint 7
@app.route("/file_retrieval_zip", methods = ['GET'])
def file_retrieval_zip():

    # zip 'retrieval' directory
    shutil.make_archive('retrieval', 'zip','./retrieval')

    # Emptying the 'retrieval' folder after sending to avoid cluttering
    if operating_system == 'Windows':
        os.system(f'del /S /q retrieval')
    else:
        os.system(f'rm -r retrieval/*') 

    return send_file("retrieval.zip")
            
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
