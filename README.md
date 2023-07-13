# Auto Update Minecraft Bedrock Server
Scripts for Automatically updating a Minecraft Bedrock edition Server.

## Requirements:
- Python 3
- Installed Bedrock Server

# Windows Usage:

## Install:

1a. Clone the repo into any folder:

```$ git clone https://github.com/vn536zl/auto-server-update.git```

1b. Or install the zip file from GitHub and extract it:

![Screenshot 2023-07-13 131118.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20131118.png)

2. Copy the files Into the directory with your Bedrock Server folder:

![copy.png](..%2F..%2FPictures%2FScreenshots%2Fcopy.png)

![Screenshot 2023-07-13 131835.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20131835.png)

## Set-up:

1. Using Notepad or any IDE edit the main.py file and replace the variables at the top:

![Screenshot 2023-07-13 132527.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20132527.png)

![Screenshot 2023-07-13 133258.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20133258.png)


2. Use Windows Task Scheduler to make a repeatable run:

![Screenshot 2023-07-13 133531.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20133531.png)

3. Select "Action > Create Basic Task":

![Screenshot 2023-07-13 133906.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20133906.png)

4. Name and describe the task:

![Screenshot 2023-07-13 133949.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20133949.png)

5. Choose when to run the task:

![Screenshot 2023-07-13 134058.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20134058.png)

![Screenshot 2023-07-13 134133.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20134133.png)

6. Choose start a program as the action:

![Screenshot 2023-07-13 134246.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20134246.png)

7. Select browse on the next screen and choose the windows_update.bat file:

![Screenshot 2023-07-13 134411.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%202023-07-13%20134411.png)

8. Click Next and Finish

You're Done the server will now update automatically (Based on when you choose to run the task)