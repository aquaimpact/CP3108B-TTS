# Text to Speech application
## Overview
This application allows users to easily convert typed text into spoken audio using the Google Cloud Text-to-Speech (TTS) API

Choose your language, the voice you want and the text you want to convert and this application will do it for you!

---

## Setting up

### Step 1:
Follow the [quick start guide](https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3#0) for Google’s TTS (From the beginning until step 2, Self-paced environment setup)

### Step 2: Set up the local [environment](https://cloud.google.com/python/docs/setup)
Follow all sections (including [Installing the Cloud Client Libraries for Python](https://cloud.google.com/python/docs/setup#installing_the_cloud_client_libraries_for_python) & [Installing the gcloud CLI](https://cloud.google.com/python/docs/setup#installing_the_cloud_sdk))**

- To setup the gcloud CLI, go to this [page](https://cloud.google.com/sdk/docs/install-sdk) and follow all the steps until [Initializing the gcloud CLI](https://cloud.google.com/sdk/docs/install-sdk#initializing_the)
- **As we will be setting this project up on our local machine, if prompted, follow the set-up instructions for local shell.

### Step 3:
Follow the [quick-start guide](https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3#0) for Google’s TTS (From Step 4 onwards)

---

## Using the application
### Step 1: Language
Enter the language you want to convert the text into and press the **Enter/Return** key. This will fetch the available voices for that language.

### Step 2: Voice
Once the language has been chosen, the dropdoen box will be populated with the list of available voices. Choose one.

### Step 3: Text
Type the text to be converted. Multi-line text is supported.

### Step 4: Output file name
Provide the output file name to be converted. The file that will be output will be a `.wav` file

### Step 5: Finding the output file
Upon the successful creation of the audio file, the path to the output file will be shown in the results section.

### Possible errors & how to solve them:
#### Error 1: (Mac)
`[Errno 30] Read-only file system: [path]`
#### Reason:
This application currently stores the audio file in the current file directory as the application. Hence, if the directory the application is in is a read only, then this error will appear.
#### Solve it:
To solve it, move the application to another directory which is also writable and rerun the application again.
