# CSCI3280_2023_Group2  
This is the group project of CSCI3280 group 2, 2023-2024 sem 2, CUHK.  

This projecthas been contributed by the following people:  
NIU Chenyu	1155173880  
QIN Jiantong	1155191496  
WANG Yitian	1155173881  
ZHANG Heqiong	1155191874

## Installation
To use this project, you need to use exactly Python version 3.10, and install the following dependencies using pip:
```
pip install pyqt5
pip install qtawesome
pip install assemblyai
pip install pyaudio  
pip install librosa
pip install matplotlib
pip install sounddevice
pip install numpy
pip install soundfile
pip install pydub
```
Notice: You may meet some issues when using pydub, "FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'". Since we are using Mac, we don't really know how to solve this issue, so please refer to some online resources to solve this problem.  

## Usage  
First, please make sure all users are using the same local area network. The network creater may set CENTRAL_SERVER_IP to the IP address of the creater's in central_server.py. Then, everybody including the creater may set CENTRAL_SERVER_IP to that IP address.  
```run``` the file GUI.py. Enter a user name you like and you do not need to enter a password. Click on Login button. This step may be failed because of some unknown features of this framework PyQt5. If the program breaks after you do so, please run it again.  
Any of the user may create a room. After one user create a room, other users may click the refresh button to find that room and double click the room to enter it. 

For the Phase II usage datails, please refer to the Phase II file CSCI3280Group2ProjectReport.pdf. Phase I files CSCI3280Group2ProjectProgress.pdf and CSCI3280Group2ProjectDemo.mp4 may also be used.  
Should you have any questions when using this program, please feel free to contact any of us.
