# ub_speech_analysis
Speech analysis script that converts audio into text and phonems

# How to install
You will require the following projects to run script
- Terminal software
- Talk bank data

## Terminal software

### wget

** Ubunutu/Debian ** 
sudo apt-get install wget

** Windows **

To install and configure wget for Windows:

    Download wget for [Windows](https://gnuwin32.sourceforge.net/packages/wget.htm) and install the package.
    Add the wget bin path to environment variables (optional). Configuring this removes the need for full paths, and makes it a lot easier to run wget from the command prompt:
        Open the Start menu and search for “environment.”
        Select Edit the system environment variables.
        Select the Advanced tab and click the Environment Variables button.
        Select the Path variable under System Variables.
        Click Edit.
        In the Variable value field add the path to the wget bin directory preceded by a semicolon (;). If installed in the default path, add C:Program Files (x86)GnuWin32bin.
    Open the command prompt (cmd.exe) and start running wget commands.

## Python libaries

** Ubunutu/Debian **
'sudo apt install python3-pip' 
'sudo apt-get install -y python3-pyfiglet'
'sudo apt-get install python3-termcolor'
'sudo apt-get install -y python3-pydub'
'sudo apt-get install python3-moviepy'

** Windows **
'py get-pip.py'
'pip install pyfiglet'
'pip install termcolor'
'pip install pydub'
'pip install moviepy'


## Talk Bank

To download file from talk bank, use the example command, or look at the ["how to download pdf"](https://talkbank.org/share/data.html):

'wget -e robots=off -R "index.html*" -N -nH -l inf -r --no-parent https://media.talkbank.org/ca/GulfWar/' - *this used to be in the pdf, but then they removed it*

The medical cases will require a username and password to access. Prof. Xu has one, but we are working one getting our own.