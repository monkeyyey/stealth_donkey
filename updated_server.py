import os, shutil, io
from flask import Flask, send_file, request
from flask import Response
from zipfile import ZipFile
from flask_cors import CORS

# Initialize + Enable Cross origin resource sharing
app = Flask(__name__)
CORS(app)

#1. send file back to server
@app.route("/sendFile")
def sendFile():
    path = "./databack/data.txt"
    return send_file(path, as_attachment=True), 201

#2. send folder back to server
@app.route("/sendZip")
def sendZip():
    directory = "./zippy"
    output_file = "compressed"
    shutil.make_archive(f'{directory}/{output_file}', 'zip',)
    return send_file(f'{directory}/{output_file}.zip', as_attachment=True), 201

#3. get file/zip file from server (URL example: http://127.0.0.1:5000/getfile?type=file)
@app.route("/getfile")
def getFile():
    
    # Retrieve URL params
    type = request.args.get('type')

    # Get file/zip file using curl
    if type == "file":
        os.system('curl --insecure https://192.168.1.81:8080/api/file/get_File > databack.txt')
        return Response(status=201)
    elif type == "zip":
        os.system(f'curl --insecure https://192.168.1.81:8080/api/file/get_Zip > compressed2.zip')
        #Code to unzip#
        return Response(status=201)

    # file type in params invalid
    return Response(status=400)

#4. Retrieve specific file(s) from client
@app.route("/file_retrieval", methods = ['POST'])
def file_retrieval():

    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    retrieval_os = request_data['retrieval_os']
    file_location = request_data['file_location']

    # Splitting the file input to check length + strip blank space
    file_location = file_location.split(',')
    for file in file_location: file = file.strip()

    # One file only
    if len(file_location) == 1:
        return send_file(f'{file_location[0]}', as_attachment=True)
    
    # More than one file  
    else:

        # copy files to 'retrieval' folder
        if retrieval_os == 'Windows':
            for file in file_location:
                file2 = file.split('\\')[-1]
                os.system(f'copy {file} retrieval\{file2}')
        else:
            for file in file_location:
                file2 = file.split('/')[-1]
                os.system(f'cp {file} ./retrieval/{file2}')
        
        # creating zip object
        fileobj = io.BytesIO()
        with ZipFile(fileobj, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk('retrieval'):
                for filename in filenames:
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath)
        fileobj.seek(0)  
        file_data = fileobj.getvalue()

        # Emptying the 'retrieval' folder after sending to avoid cluttering
        if retrieval_os == 'Windows':
            os.system(f'del /S /q retrieval')
        else:
            os.system(f'rm -r retrieval/*')   

        return Response(file_data, mimetype='application/zip', headers={'Content-Disposition': 'attachment;filename=retrieval.zip'})

#5. Command Execution + output to file
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

#6. Collection of specific files + copy to specific folder
@app.route("/file_collection", methods = ['POST'])
def file_collection():

    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    operating_system = request_data['OS']
    output_destination = request_data['output']
    collect = request_data['collect']
    files = request_data['files']

    # Splitting the file input to check length + strip blank space
    files = files.split(',')
    for file in files: file = file.strip()

    # copy files to outout destination
    if operating_system == 'Windows':
        for file in files:
            os.system(f'copy {file} {output_destination}')
    else:
        for file in files:
            os.system(f'cp {file} ./{output_destination}')
    
    # zip files in output destination
    shutil.make_archive(f'collection', 'zip', f'{output_destination}')
    if collect == "Yes":
        return send_file(f'{output_destination}/collection.zip', as_attachment=True)
    
    return Response(status=201)

#7. Send files to another server via SSH
@app.route("/ssh_send", methods = ['POST'])
def ssh_send():

    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    ssh_os = request_data['ssh_OS']
    ssh_ip = request_data['ssh_ip']
    ssh_user = request_data['ssh_user']
    ssh_pass = request_data['ssh_pass']
    ssh_files = request_data['ssh_files']
    ssh_output = request_data['ssh_output']

    # Setting commands based on operating system
    if ssh_os == 'Windows':
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
    if ssh_os == 'Windows':
        os.system(f'del /S /q send_ssh')
    else:
        os.system(f'rm -r send_ssh/*')
        
    return Response(status=201)

#7. Retrieve specific file(s) from client
@app.route("/file_retrieval", methods = ['POST'])
def file_retrieval():

    # Retreive JSON data + Assign variables
    request_data = request.get_json()
    retrieval_os = request_data['retrieval_os']
    file_location = request_data['file_location']

    # Splitting the file input to check length + strip blank space
    file_location = file_location.split(',')
    for file in file_location: file = file.strip()

    # One file only
    if len(file_location) == 1:
        return send_file(f'{file_location[0]}', as_attachment=True)
    
    # More than one file  
    else:

        # copy files to 'retrieval folder'
        if retrieval_os == 'Windows':
            for file in file_location:
                file2 = file.split('\\')[-1]
                os.system(f'copy {file} retrieval\{file2}')
        else:
            for file in file_location:
                file2 = file.split('/')[-1]
                os.system(f'cp {file} ./retrieval/{file2}')
        
        # creating zip object
        fileobj = io.BytesIO()
        with ZipFile(fileobj, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk('retrieval'):
                for filename in filenames:
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath)
        fileobj.seek(0)  
        file_data = fileobj.getvalue()

        # Emptying the 'retrieval' folder after sending to avoid cluttering
        if retrieval_os == 'Windows':
            os.system(f'del /S /q retrieval')
        else:
            os.system(f'rm -r retrieval/*')   

        return Response(file_data, mimetype='application/zip', headers={'Content-Disposition': 'attachment;filename=retrieval.zip'})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
