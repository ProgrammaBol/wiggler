@echo  #---------------------------------------------#
@echo  # wiggler prerequisites installer for Windows #
@echo  #---------------------------------------------#

@echo off
:: detect windows architecture and set up variables accordingly to prerequisites to download
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

set pversion=0

::detect installed powershell version (if any) to use specific command in order to download requested prerequisites
for /f %%i in ('powershell -Command $PSVersionTable.PSVersion.Major') do set pversion=%%i

md installer
echo  # installing Python 2.7 #

If %pversion% GEQ 3 goto win8+ 
If %pversion% GEQ 2 goto win7
If %pversion% GEQ 0 goto winxp

:win8+
IF NOT EXIST installer\%PYNAME% powershell -Command Invoke-WebRequest %ADDRPY% -OutFile installer\%PYNAME%
goto end
:win7
IF NOT EXIST installer\%PYNAME% powershell (New-Object System.Net.WebClient).DownloadFile('%ADDRPY%', 'installer\%PYNAME%')
goto end
:winxp
echo.
echo ####################
echo ## IMPORTANT NOTE ##
echo ############################################################
echo ## This installation script needs PowerShell 2 or higher. ##
echo ##      See docs/installing.md for further reference      ##
echo ############################################################
goto exit
:end

echo  IMPORTANT: during setup, while selecting features to install, select ADD python.exe TO PATH
echo  NOTE: REMEMBER Python INSTALLATION DIR
msiexec /i installer\%PYNAME%

:: ask user for installation dir and set path properly
set PYPATH=C:\Python27
set PYSCRIPTS=C:\Python27\Scripts
set /P INPUT=Is Python installation dir %PYPATH%?(Y/N): %=%
If /I "%INPUT%"=="y" goto yes 
If /I NOT "%INPUT%"=="y" goto no
:no
set /P PYPATH=Insert Python path: %=%
:yes
set PATH=%PATH%;%PYPATH%;%PYSCRIPTS%

:: installing other software
pip install --upgrade pip
echo  #   installing PyGame   #

If %pversion% GEQ 3 goto win8+ 
If %pversion% GEQ 2 goto win7
If %pversion% GEQ 0 goto winxp

:win8+
IF NOT EXIST installer\%PYGNAME% powershell -Command Invoke-WebRequest %ADDRPYG% -OutFile installer\%PYGNAME%
goto end
:win7
IF NOT EXIST installer\%PYGNAME% powershell (New-Object System.Net.WebClient).DownloadFile('%ADDRPYG%', 'installer\%PYGNAME%')
goto end
:winxp
echo.
echo ####################
echo ## IMPORTANT NOTE ##
echo ############################################################
echo ## This installation script needs PowerShell 2 or higher. ##
echo ##      See docs/installing.md for further reference      ##
echo ############################################################
goto exit
:end

pip install installer\%PYGNAME%

echo  # installing Setuptools #

If %pversion% GEQ 3 goto win8+ 
If %pversion% GEQ 2 goto win7
If %pversion% GEQ 0 goto winxp

:win8+
IF NOT EXIST installer\ez_setup.py powershell -Command Invoke-WebRequest https://bootstrap.pypa.io/ez_setup.py -OutFile installer\ez_setup.py
goto end
:win7
IF NOT EXIST installer\ez_setup.py powershell (New-Object System.Net.WebClient).DownloadFile('https://bootstrap.pypa.io/ez_setup.py', 'installer\ez_setup.py')
goto end
:winxp
echo.
echo ####################
echo ## IMPORTANT NOTE ##
echo ############################################################
echo ## This installation script needs PowerShell 2 or higher. ##
echo ##      See docs/installing.md for further reference      ##
echo ############################################################
goto exit
:end

python ./installer/ez_setup.py >nul

del setuptools* 

echo  #  installing wxPython  #

If %pversion% GEQ 3 goto win8+ 
If %pversion% GEQ 2 goto win7
If %pversion% GEQ 0 goto winxp

:win8+
IF NOT EXIST installer\%OUTWX% powershell -Command Invoke-WebRequest -Uri %URLWX% -OutFile installer\%OUTWX% -UserAgent [Microsoft.PowerShell.Commands.PSUserAgent]::FireFox
goto end
:win7
IF NOT EXIST installer\%OUTWX% powershell (New-Object System.Net.WebClient).DownloadFile('%URLWX%', 'installer\%OUTWX%')
goto end
:winxp
echo.
echo ####################
echo ## IMPORTANT NOTE ##
echo ############################################################
echo ## This installation script needs PowerShell 2 or higher. ##
echo ##      See docs/installing.md for further reference      ##
echo ############################################################
goto exit
:end
echo IMPORTANT: during setup, select full installation and all the defalut options
.\installer\%OUTWX%

echo  #   installing Jinja2   #
pip install jinja2
echo  #   installing PyYAML   #
pip install pyyaml

:exit
@echo on
