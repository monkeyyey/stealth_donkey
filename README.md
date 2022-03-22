# stealth_donkey
Stealth Donkey is a work-in-progress Proof-of-Concept(POC) project, a framework which can be applied to gather runtime system configuration and status for a targeted system at the stealth mode.

The framework should be able to be customizable for various OS and/or type of information to be collected. 

With the framework in place, a system administrator can apply it to monitor and gather vital system information for malware and/or intrusion detection at the EndPoint level. 

References:
1.	Unisys Stealth Solution Release v4.0: https://www.commoncriteriaportal.org/files/epfiles/st_vid10989-st.pdf
2.	A Comprehensive Open Source Security Platform: https://wazuh.com/

## Definitions
Agent:
Admin Server:
Client/Client Machine:

## Technical Prerequisites
### 1. Install Agent dependencies <br />
The requirements file is in the Agent Branch, remember to cd to the Agent directory!<br />
No need to install dependencies in the Admin server, they are in the node_modules folder (i think).
```
pip install -r requirements.txt
```
### 2. Setting up Client Machine

### 3. Setting up SSH server

## Good-to-Know 
### 1. The Folders required in Agent Branch are not there
Folders to create in /Agent Directory before testing: /databack, /retrieval, /send_ssh
### 2. Both the Agent and Admin are 'servers' and 'clients'
As they exchange information with each other, they both require endpoints. Difference is that Admin server has Web interface.
### 3. Ur mum is gae
Yup.

## Things to learn before starting
### 1. Using Flask (Python version of Express node.js)
Our current Agent Server is created using Flask.
### 2. Executing OS commands using code
Most of the functionalities are made possible by using OS commands <br />
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

## Agent Server Endpoints summary
1 and 2 are experimental endpoints used to send a file/zipfile to Admin server. <br />
3 and 4 are endpoints used to download a file/zipfile from Admin server. <br />
5 is and endpoint for command execution on the Client, with the choice to save the result in a specific location on the Client. <br />
  
## Agent Server Endpoints 
### 1. Hard coded endpoint that sends back file
Upon receiving get request, it sends back a downloadable file by referring to a hard coded variable.
### 2. Hard coded endpoint that sends back zip file
Upon receiving get request, it zips a folder and sends back a downloadable zip file by referring to hard coded variables.
  
## To be Fixed/Tested/Solved
### 1. Operating system compatibility (Applicable for Agent endpoints 5,6,7,8)
There is a problem regarding how to traverse directories in Windows. For example, entering location to output a file in linux may look something like this: "./animal/money.txt". In windows, some commands require the input to look like this "animal\money.txt". From my experience, this is very inconsistent across different commands. <br />
In summary, just fix this problem by testing and tweaking the code.
### 2. How to automate answering of OS command replies (Applicable to Agent Endpoints)
Right now, I can only execute OS commands, but I am unable to answer anything AFTER the command is executed. For Example, I am unable to execute commands like SSH logins, where I need to enter a password after I enter the SSH commands.<br />
I have managed to use workarounds for these problems like SSHPASS and adding --insecure to curl commands. But some workarounds may require the Client machine to install certain services, which is not practical from the client perspective as our agent is supposed to be 'Stealthy'
### 3. How to download files directly to folder (Applicable to Admin Endpoints in home.html)
Right now, files that are received by the Admin from the Agent is downloadable files, but this requires user action to choose where the folder is downloaded. Automating this is more practical from Admin perspective.



