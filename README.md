# EchoMind
Speech analysis script that converts audio into text and phonems
  
    
![Temp logo](/project_resources/logo_ver2.png "Temp logo")


# How to install
You will require the following projects to run script
- Terminal software
- Talk bank data

## Terminal software

### wget

**Ubunutu/Debian** 

` sudo apt-get install wget `

**Windows**

To install and configure wget for Windows:

    Download wget for [Windows](https://gnuwin32.sourceforge.net/packages/wget.htm "Windows") and install the package.
    Add the wget bin path to environment variables (optional). Configuring this removes the need for full paths, and makes it a lot easier to run wget from the command prompt:
        Open the Start menu and search for “environment.”
        Select Edit the system environment variables.
        Select the Advanced tab and click the Environment Variables button.
        Select the Path variable under System Variables.
        Click Edit.
        In the Variable value field add the path to the wget bin directory preceded by a semicolon (;). If installed in the default path, add C:Program Files (x86)GnuWin32bin.
    Open the command prompt (cmd.exe) and start running wget commands.


### ffmeg

**Ubunutu/Debian** 

` sudo apt update && sudo apt install ffmpeg `

**Windows**

On Windows using Chocolatey (https://chocolatey.org/)
` choco install ffmpeg `

On Windows using Scoop (https://scoop.sh/)
` scoop install ffmpeg `

## Python libaries

**Ubunutu/Debian**
``` 
sudo apt install python3-pip
sudo apt-get install -y python3-pyfiglet
sudo apt-get install python3-termcolor
sudo apt-get install -y python3-pydub
sudo apt-get install python3-moviepy 
sudo apt install python3-numpy
```

**Windows**
``` 
py get-pip.py
pip install pyfiglet
pip install termcolor
pip install pydub
pip install moviepy
pip install numpy 
```


## Allosaurus
To install Allosaurus, use the pip command, or install it from the [git reop](https://itsfoss.com/markdown-code-block/ "git repo")

` pip install allosaurus `

Then you will need to install a model for it to run. The script is set to the english model which will require you to download it 

` python3 -m allosaurus.bin.download_model -m eng2102 `

However you can download and use other models if you wish


## Vosk

You can install Vosk through the pip command:

` pip3 install vosk `

Further more you will need to download a [Model](https://alphacephei.com/vosk/models "Model"), unpack it, and update the scipt line

  `"modelV_path = "/home/parallels/Downloads/vosk-model-en-us-0.22-lgraph" " `

,to point to the correct path.

## Wishper

To install whisper use the pip command :

` pip install -U openai-whisper `

## whisper-timestamped

Install using pip command 

` pip3 install git+https://github.com/linto-ai/whisper-timestamped `

light weight version of tourch for cpu proccessing as oppesed to gpu processing

``` 
pip3 install \
     torch==1.13.1+cpu \
     torchaudio==0.13.1+cpu \
     -f https://download.pytorch.org/whl/torch_stable.html
```
Update to latest version
` pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/linto-ai/whisper-timestamped `


## Talk Bank

To download file from talk bank, use the example command, or look at the [how to download pdf](https://talkbank.org/share/data.html "download pdf"):

` wget -e robots=off -R "index.html*" -N -nH -l inf -r --no-parent https://media.talkbank.org/ca/GulfWar/ ` - *this used to be in the pdf, but then they removed it*

The medical cases will require a username and password to access. Prof. Xu has one, but we are working one getting our own.