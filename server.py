import os
import shutil
import io
from flask import Flask, send_file, request
from flask import Response
from zipfile import ZipFile
from flask_cors import CORS
# return Response("{'a':'b'}", status=201, mimetype='application/json')

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

#3. get file from server
@app.route("/getFile")
def getFile():
    os.system('curl --insecure https://192.168.1.81:8080/api/file/get_File > databack.txt')
    return Response(status=201)

#4. get folder from server
@app.route("/getZip")
def getZip():
    os.system(f'curl --insecure https://192.168.1.81:8080/api/file/get_Zip > compressed2.zip')
    return Response(status=201)

#5. Command Execution + output to file
@app.route("/command", methods = ['POST'])
def command():
    request_data = request.get_json()
    command = request_data['cmd']
    exec_only = request_data['exec_only']
    if exec_only == 'No':
        output_destination = request_data['command_output']
        os.system(f'{command} > {output_destination}')
    else:
        os.system(f'{command}')
    return Response(status=201)

#6. Collection of specific files + copy to specific folder
@app.route("/file_collection", methods = ['POST'])
def file_collection():

    request_data = request.get_json()
    print(request_data)
    operating_system = request_data['OS']
    files = request_data['files']
    output_destination = request_data['output']
    collect = request_data['collect']
    if collect == "Yes":
        zipfile = request_data['zipfile']
    
    if operating_system == 'Windows':
        os.system(f'mkdir {output_destination}/{zipfile}')
        for file in files.split(','):
            file = file.strip()
            os.system(f'copy {file} {output_destination}\{zipfile}')
    else:
        os.system(f'mkdir {output_destination}/{zipfile}')
        for file in files.split(','):
            file = file.strip()
            file2 = file.split('/')[-1]
            os.system(f'cp {file} ./{output_destination}/{zipfile}')
    shutil.make_archive(f'{output_destination}/{zipfile}', 'zip', f'{output_destination}/{zipfile}')
    if collect == "Yes":
        return send_file(f'{output_destination}/{zipfile}.zip', as_attachment=True)
    return Response(status=201)

#7. Send files to another server via SSH
@app.route("/ssh_send", methods = ['POST'])
def ssh_send():

    request_data = request.get_json()
    ssh_os = request_data['ssh_OS']
    ssh_ip = request_data['ssh_ip']
    ssh_user = request_data['ssh_user']
    ssh_pass = request_data['ssh_pass']
    ssh_files = request_data['ssh_files']
    ssh_output = request_data['ssh_output']

    if ssh_os == 'Windows':
        copy = 'copy'
        delete = 'del /f'
    else:
        copy = 'cp'
        delete = 'rm'
    
    for file in ssh_files.split(','):
        file = file.strip()
        file2 = file.split('/')[-1]
        os.system(f'{copy} {file} ./send_ssh/{file2}')
    shutil.make_archive(f'send_ssh', 'zip', 'send_ssh')
    os.system(f'sshpass -p "{ssh_pass}" scp send_ssh.zip {ssh_user}@{ssh_ip}:{ssh_output}')
    os.system(f'{delete} send_ssh.zip')
    if ssh_os == 'Windows':
        os.system(f'del /S send_ssh')
    else:
        os.system(f'rm -r send_ssh/*')
    return Response(status=201)

#8. Retrieve specific file(s) from client
@app.route("/file_retrieval", methods = ['POST'])
def file_retrieval():
    request_data = request.get_json()
    retrieval_os = request_data['retrieval_os']
    print(retrieval_os  )
    file_location = request_data['file_location']
    file_location = file_location.split(',')
    if len(file_location) == 1:
        return send_file(f'{file_location[0]}', as_attachment=True)
    else:
        if retrieval_os == 'Windows':
            copy = 'copy'
            for file in file_location:
                file = file.strip()
                file2 = file.split('\\')[-1]
                print(file,file2)
                cmd = f'{copy} {file} retrieval\{file2}'
                os.system(cmd)
        else:
            copy = 'cp'
            for file in file_location:
                file = file.strip()
                file2 = file.split('/')[-1]
                print(file,file2)
                cmd = f'{copy} {file} ./retrieval/{file2}'
                os.system(cmd)
        fileobj = io.BytesIO()
        with ZipFile(fileobj, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk('retrieval'):
                for filename in filenames:
                    #create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath)
        fileobj.seek(0)  
        file_data = fileobj.getvalue()
        if retrieval_os == 'Windows':
            os.system(f'del /S /q retrieval')
        else:
            os.system(f'rm -r retrieval/*')   
        return Response(file_data,
                        mimetype='application/zip',
                        headers={'Content-Disposition': 'attachment;filename=retrieval.zip'})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')