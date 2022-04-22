# stealth_donkey
Work-in-progress framework that can be applied to gather runtime system configuration and status for a targeted system at the stealth mode.

With the framework in place, a system administrator can monitor and gather vital system information for malware and/or intrusion detection at the EndPoint level.

References:
1.	Unisys Stealth Solution Release v4.0: https://www.commoncriteriaportal.org/files/epfiles/st_vid10989-st.pdf
2.	A Comprehensive Open Source Security Platform: https://wazuh.com/
3.	WAZUH source code: https://github.com/wazuh/wazuh

<br /><br />
## Definitions
`Agent`: Script running on Client Machine <br />
`Client`/`Client Machine`: Machine which the Agent is monitoring <br />
`Admin Server`: Administrative server that communicates with Agent, has a web interface

<br /> <br />
## Diagram of Current architecture
### 1. With Online Agent
For Online Agent, Admin sends instructions to the Agent. <br /><br />
![alt text](https://github.com/monkeyyey/stealth_donkey/blob/main/git_images/agent.PNG)
### 2. With Local Agent
For Online Agent, instructions are read from a local file. <br /><br />
![alt text](https://github.com/monkeyyey/stealth_donkey/blob/main/git_images/local_agent.PNG)
<br />
We may combine the 2 different functionalities after finishing both of these.


<br /><br />
## Technical Prerequisites


### 1. Install Agent dependencies <br />
\**This step only applies if you are installing agent on Oracle or any other Linux distros*\* <br />
The requirements file is in the Agent Branch, remember to `cd` to the `Agent` directory!
```
pip install -r oracle_requirements.txt
```
No need to install dependencies in the `Admin Server`, they are in the node_modules folder (i think).
<br /><br />

### 2. Configure Models/DatabaseConfig.js
Modify so that you can connect to your mysql databasae
<br /><br />


### 3. Setting up Client Machine

#### i. Installing sshpass 
`sshpass` is used to include password in `scp` request, to prevent prompt for password.
```
# For safe measure, update + upgrade
yum update
yum upgrade

# Need epel-release to install sshpass
yum install epel-release
yum install sshpass 
```

#### ii. Adding Agent as systemd service
This ensures that `Agent` is able to run in background, upon startup. Change the `<names>` and `<filepaths>` to what is appropriate for you. <br /> <br />
Create `.service` file:
```
cd /etc/systemd/system
touch <service_name>.service
```
Open the `.service` file in a file editor and enter this:
```
[Unit]
Description=Stealth agent that monitor ur fat ass
After=network.target

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
ExecStart=python3 <Full_file_path_Directory_Only>/server.py
WorkingDirectory= <Full_file_path_Directory_Only>
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=%n
```
Reload the system daemon + start the service:
```
sudo systemctl daemon-reload
sudo systemctl enable <service_name>.service
sudo systemctl start <service_name>.service
```
`After=network.target` in service file ensures that service starts only when there is internet connection, may need to change this when configuring 'static Agents' later on. <br />
`systemctl enable` ensures that service always starts upon bootup.
<br /><br />

### 3. Setting up SSH server
SSH server for storage of files that Admin wants to save, for endpoint 7. The SSH server will be set-up on a Kali Linux machine.
<br />
<br />
Install SSH server + Start ssh service:
```
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```
Ensure SSH server is running, `netstat -tupln`:
```
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8834            0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::8834                 :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -      
```
SSH runs on port `22`, so just check ah brother.


<br /><br />
## Good-to-Know 

### 1. Both the Agent and Admin are 'servers' and 'clients'
As they exchange information with each other, they both require endpoints. Difference is that `Admin Server` has Web interface.

### 2. Operating System Compatibility
At the current stage, the OS compatibility of Agent is only so that you can easily use vscode to edit and run the Agent on local machine, and maybe to impress KK. Our final project will be mainly focused on Oracle Linux.

### 3. Ur mum is gae
Yup.


<br /><br />
## Things to learn before starting

### 1. Using Flask (Python version of Express node.js)
Our current Agent Server is created using Flask.

### 2. Executing OS commands using code
Most of the functionalities are made possible by using OS commands <br /> <br />
Python:
```
os.system("<Command>")
```
Javascript:
```
exec("<Command>")
```

### 3. Using the Agent to monitor system information to detect malware and intrusion detection
Currently have zero knowledge on this. This component is the most important, as it serves the main purpose of this project.


<br /><br />
## Agent Endpoints summary
`1` is an endpoints used to download a file/zipfile from `Admin server`. <br /><br />
`2` is an endpoint for command execution on the `Client`, with the choice to save the result in a specific location on the `Client`. <br /><br />
`3` is an endpoint for collecting specific files on the `Client`, and copying them to a specific folder, with the choice to retrieve this folder as a zip file.<br /><br />
`4` is an endpoint for collecting specific files on the `Client`, and sending them to an SSH server as a zip file. <br /> <br />
`5` is an endpoint for collecting specific files on client straight back to `Admin Server`. <br /> <br />
`6` and `7` are follow up endpoints from endpoint `5` to send the file/zipfile to admin server

### For endpoint `5`, `6`, `7`: <br />
`5` Receives request for file collection, copy files to 'retrieval' folder (if there are multiple files)
`Admin Server` creates another request to own backend `controllers/exec.js`, which makes a curl request to `Agent` endpoint `6` and `7`, depending on whether there are one or more than one files to retrieve <br />
`6` or `7` then sends the file/zip file back to `Admin Server`


<br /><br />
## To be Fixed/Tested/Solved

### 1. How to automate answering of OS command replies (Applicable to Agent Endpoints)
Right now, I can only execute OS commands, but I am unable to answer anything AFTER the command is executed. For Example, I am unable to execute commands like SSH logins, where I need to enter a password after I enter the SSH commands.<br />
I have managed to use workarounds for these problems like `sshpass` and adding `--insecure` to curl commands. But some workarounds may require the Client machine to install certain services, which is not practical from the client perspective as our agent is supposed to be 'Stealthy'.

### 2. Automatically run Agent functions at time intervals
Now only can read from local, then admin activate by clicking button. Need to make it run automatically at time intervals

