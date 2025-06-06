@echo off
:: === Check for admin rights ===
>nul 2>&1 net session
if %errorlevel% NEQ 0 (
    echo [INFO] Elevating to administrator...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

echo [INFO] Running with administrative privileges.

SETLOCAL

:: Check if choco is installed
where choco >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo Chocolatey is already installed.
) ELSE (
    echo Chocolatey not found. Installing...

    :: Use PowerShell to install Chocolatey
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

    :: Check again
    where choco >nul 2>nul
    IF %ERRORLEVEL% EQU 0 (
        echo Chocolatey installed successfully.
    ) ELSE (
        echo Failed to install Chocolatey.
    )
)

ENDLOCAL
pause

:: === User Creation Block ===

SETLOCAL

:: === Rename Current User ===
echo Renaming current user %USERNAME% to Admin...
wmic useraccount where name="%USERNAME%" rename "Admin"
net user "Admin" /fullname:"Admin"

:: === Create User: Profile1 ===
echo Creating user Profile1...
net user "Profile1" "Temp1234" /add
net localgroup "Users" "Profile1" /add

:: === Trigger profile creation ===
runas /user:Profile1 "cmd /c echo Profile initialized for Profile1"

:: === Create User: Profile2 ===
echo Creating user Profile2...
net user "Profile2" "Temp1234" /add
net localgroup "Users" "Profile2" /add

:: === Trigger profile creation ===
runas /user:Profile2 "cmd /c echo Profile initialized for Profile2"

ENDLOCAL

pause


:: === Folder Setup for Admin ===
IF EXIST C: (
    mkdir "C:\Admin"
    mkdir "C:\Admin\PerfLogs"
    mkdir "C:\Admin\Program Files"
    mkdir "C:\Admin\Program Files (x86)"
    mkdir "C:\Admin\Users"
    mkdir "C:\Admin\Windows"
    mkdir "C:\Admin\XboxGames"
    :: Set permissions for Admin and Admin
    icacls "C:\Admin" /inheritance:r
    icacls "C:\Admin" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive C: not found. Skipping folder creation.
)
IF EXIST D: (
    mkdir "D:\Admin"
    :: Set permissions for Admin and Admin
    icacls "D:\Admin" /inheritance:r
    icacls "D:\Admin" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive D: not found. Skipping folder creation.
)
IF EXIST E: (
    mkdir "E:\Admin"
    :: Set permissions for Admin and Admin
    icacls "E:\Admin" /inheritance:r
    icacls "E:\Admin" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive E: not found. Skipping folder creation.
)

:: === Folder Setup for Profile1 ===
IF EXIST C: (
    mkdir "C:\Profile1"
    mkdir "C:\Profile1\PerfLogs"
    mkdir "C:\Profile1\Program Files"
    mkdir "C:\Profile1\Program Files (x86)"
    mkdir "C:\Profile1\Users"
    mkdir "C:\Profile1\Windows"
    mkdir "C:\Profile1\XboxGames"
    :: Set permissions for Profile1 and Admin
    icacls "C:\Profile1" /inheritance:r
    icacls "C:\Profile1" /grant Profile1:"(OI)(CI)F"
    icacls "C:\Profile1" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive C: not found. Skipping folder creation.
)
IF EXIST D: (
    mkdir "D:\Profile1"
    :: Set permissions for Profile1 and Admin
    icacls "D:\Profile1" /inheritance:r
    icacls "D:\Profile1" /grant Profile1:"(OI)(CI)F"
    icacls "D:\Profile1" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive D: not found. Skipping folder creation.
)
IF EXIST E: (
    mkdir "E:\Profile1"
    :: Set permissions for Profile1 and Admin
    icacls "E:\Profile1" /inheritance:r
    icacls "E:\Profile1" /grant Profile1:"(OI)(CI)F"
    icacls "E:\Profile1" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive E: not found. Skipping folder creation.
)

:: === Folder Setup for Profile2 ===
IF EXIST C: (
    mkdir "C:\Profile2"
    mkdir "C:\Profile2\PerfLogs"
    mkdir "C:\Profile2\Program Files"
    mkdir "C:\Profile2\Program Files (x86)"
    mkdir "C:\Profile2\Users"
    mkdir "C:\Profile2\Windows"
    mkdir "C:\Profile2\XboxGames"
    :: Set permissions for Profile2 and Admin
    icacls "C:\Profile2" /inheritance:r
    icacls "C:\Profile2" /grant Profile2:"(OI)(CI)F"
    icacls "C:\Profile2" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive C: not found. Skipping folder creation.
)
IF EXIST D: (
    mkdir "D:\Profile2"
    :: Set permissions for Profile2 and Admin
    icacls "D:\Profile2" /inheritance:r
    icacls "D:\Profile2" /grant Profile2:"(OI)(CI)F"
    icacls "D:\Profile2" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive D: not found. Skipping folder creation.
)
IF EXIST E: (
    mkdir "E:\Profile2"
    :: Set permissions for Profile2 and Admin
    icacls "E:\Profile2" /inheritance:r
    icacls "E:\Profile2" /grant Profile2:"(OI)(CI)F"
    icacls "E:\Profile2" /grant Admin:"(OI)(CI)F"
) ELSE (
    echo Drive E: not found. Skipping folder creation.
)

:: === Global App Folders Setup ===
IF EXIST C: (
    mkdir "C:\Apps"
    mkdir "C:\Apps\"
    mkdir "C:\Apps\\Steam"
    mkdir "C:\Apps\\Winrar"
    mkdir "C:\Apps\\Chrome"
    mkdir "C:\Apps\\Firefox"
    mkdir "C:\Apps\\Matlab"
    mkdir "C:\Apps\\Notepad_plus"
) ELSE (
    echo Drive C: not found. Skipping folder creation.
)
IF EXIST D: (
    mkdir "D:\Apps"
    mkdir "D:\Apps\"
) ELSE (
    echo Drive D: not found. Skipping folder creation.
)
IF EXIST E: (
    mkdir "E:\Apps"
    mkdir "E:\Apps\"
) ELSE (
    echo Drive E: not found. Skipping folder creation.
)

:: === Global App Install ===
IF EXIST "C:\Apps\Steam" (
    choco install steam -y --ignore-checksums --params "/InstallDir=C:\Apps\Steam"
) ELSE (
    echo Folder C:\Apps\Steam not found. Skipping install for steam.
)
IF EXIST "C:\Apps\Winrar" (
    choco install winrar -y --ignore-checksums --params "/InstallDir=C:\Apps\Winrar"
) ELSE (
    echo Folder C:\Apps\Winrar not found. Skipping install for winrar.
)
IF EXIST "C:\Apps\Chrome" (
    choco install GoogleChrome -y --ignore-checksums --params "/InstallDir=C:\Apps\Chrome"
) ELSE (
    echo Folder C:\Apps\Chrome not found. Skipping install for GoogleChrome.
)
IF EXIST "C:\Apps\Firefox" (
    choco install Firefox -y --ignore-checksums --params "/InstallDir=C:\Apps\Firefox"
) ELSE (
    echo Folder C:\Apps\Firefox not found. Skipping install for Firefox.
)
IF EXIST "C:\Apps\Matlab" (
    choco install mcr-r2022b -y --ignore-checksums --params "/InstallDir=C:\Apps\Matlab"
) ELSE (
    echo Folder C:\Apps\Matlab not found. Skipping install for mcr-r2022b.
)
IF EXIST "C:\Apps\Notepad_plus" (
    choco install notepadplusplus -y --ignore-checksums --params "/InstallDir=C:\Apps\Notepad_plus"
) ELSE (
    echo Folder C:\Apps\Notepad_plus not found. Skipping install for notepadplusplus.
)