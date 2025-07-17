# Text to Speech application
## Overview
This application allows users to easily convert typed text into spoken audio using the Google Cloud Text-to-Speech (TTS) API

Choose your language, the voice you want and the text you want to convert and this application will do it for you!

---

## Setting up

### Enabling Google TTS
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project if you havent already done so
3. Under the Quick access, click APIs & Services ![Google's API & Services](/User%20Guide/image.png)
4. Enable APIs and Serices ![alt text](/User%20Guide/image-1.png)
5. Search for Text to Speech API ![alt text](/User%20Guide/image-2.png)
6. Enable it ![alt text](/User%20Guide/image-3.png)
  ** You may have to setup billing account

### Getting a service account
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Using the navigation menu on the left, click on APIs & Services > Credentials ![alt text](/User%20Guide/image-6.png)
4. Select Create credentials > Service account ![alt text](/User%20Guide/image-7.png)
5. Create Service account name
![alt text](/User%20Guide/image-8.png)
6. Under the Permissions section, select the Cloud Speech-to-Text Service Agent ![alt text](/User%20Guide/image-9.png)
7. Click Done

### Creating credentials.json and adding it to the application
1. Go into the service account you just created![alt text](/User%20Guide/image-4.png)
2. Go to the Keys tab ![alt text](/User%20Guide/image-5.png)
3. Create a new key ![alt text](/User%20Guide/image-11.png) 
4. Click JSON > Create
5. Select where you want to store this credentials file.
---

## Using the application

![alt text](/User%20Guide/image-12.png)

### Step 1: Google TTS Credentials path
Enter the path which your credentials is located in (see above for help on how to get it)

### Step 2: Language
Enter the language you want to convert the text into and press the **Enter/Return** key. This will fetch the available voices for that language.

### Step 3: Voice
Once the language has been chosen, the dropdoen box will be populated with the list of available voices. Choose one.

### Step 4: Text
Type the text to be converted. Multi-line text is supported.

### Step 5: Output file name
Provide the output file name to be converted. The file that will be output will be a `.wav` file

### Step 6: Finding the output file
Upon the successful creation of the audio file, the path to the output file will be shown in the results section.

### Possible errors & how to solve them:
#### Error 1: (Mac)
`[Errno 30] Read-only file system: [path]`
#### Reason:
This application currently stores the audio file in the current file directory as the application. Hence, if the directory the application is in is a read only, then this error will appear.
#### Solve it:
To solve it, move the application to another directory which is also writable and rerun the application again.
