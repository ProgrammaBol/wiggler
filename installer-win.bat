@echo  #---------------------------------------------#
@echo  # slither prerequisites installer for Windows #
@echo  #---------------------------------------------#

@echo off
:: detect windows architecture and set up variables accordingly 
if %PROCESSOR_ARCHITECTURE%==AMD64 (
    set ADDRPY=https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi 
	set PYNAME=python-2.7.12.amd64.msi 
	set ADDRPYG=https://pypi.python.org/packages/c2/c1/2e935144ecee8edb9edd52891467d2be5686c4c1f38e5b74de9d6a8f7c49/pygame-1.9.2b1-cp27-cp27m-win_amd64.whl
	set PYGNAME=pygame-1.9.2b1-cp27-cp27m-win_amd64.whl
	set URLWX=http://downloads.sourceforge.net/project/wxpython/wxPython/3.0.2.0/wxPython3.0-win64-3.0.2.0-py27.exe
    set OUTWX=wxPython3.0-win64-3.0.2.0-py27.exe
) else (
    set ADDRPY=https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi
    set PYNAME=python-2.7.12.msi
	set ADDRPYG=https://pypi.python.org/packages/49/d7/e48d747d5ff3c95269ec365897bd24519dffca59530ac1fb924af0f2b8f4/pygame-1.9.2b1-cp27-cp27m-win32.whl
	set PYGNAME=pygame-1.9.2b1-cp27-cp27m-win32.whl
	set URLWX=https://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/wxPython3.0-win32-3.0.2.0-py27.exe
    set OUTWX=wxPython3.0-win32-3.0.2.0-py27.exe
)

md installer
echo  # installing Python 2.7 #
IF NOT EXIST installer\%PYNAME% powershell -Command Invoke-WebRequest %ADDRPY% -OutFile installer\%PYNAME%
echo  NOTE: REMEMBER Python INSTALLATION DIR
msiexec /i installer\%PYNAME%

:: ask user for installation dir and set path properly
set PYPATH=C:\Python27
set /P INPUT=Is Python installation dir %PYPATH%?(Y/N): %=%
If /I "%INPUT%"=="y" goto yes 
If /I NOT "%INPUT%"=="y" goto no
:no
set /P PYPATH=Insert Python path: %=%
:yes
set PATH=%PATH%;%PYPATH%

:: installing other software
pip install --upgrade pip
echo  #   installing PyGame   #
IF NOT EXIST installer\%PYGNAME% powershell -Command Invoke-WebRequest %ADDRPYG% -OutFile installer\%PYGNAME%
pip install installer\%PYGNAME%

echo  # installing Setuptools #
IF NOT EXIST installer\ez_setup.py powershell -Command Invoke-WebRequest https://bootstrap.pypa.io/ez_setup.py -OutFile installer\ez_setup.py
python ./installer/ez_setup.py >nul

del setuptools* 

echo  #  installing wxPython  #
IF NOT EXIST installer\%OUTWX% powershell -Command Invoke-WebRequest -Uri %URLWX% -OutFile installer\%OUTWX% -UserAgent [Microsoft.PowerShell.Commands.PSUserAgent]::FireFox
.\installer\%OUTWX%

echo  #   installing jinja2   #
pip install jinja2
@echo on
