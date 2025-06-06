from pathlib import Path

def create_base_all_profiles_cmd():
    current_script_path = Path(__file__).resolve()
    root_dir = current_script_path.parent.parent
    input_json = root_dir / "preset_config.json"

    output_cmd = current_script_path.parent / "all_profiles.cmd"

    choco_block = r"""@echo off
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
"""

    with open(output_cmd, "w", encoding="utf-8") as f:
        f.write(choco_block)

    print(f"✅ Created base script: {output_cmd}")

# === Entry point ===
if __name__ == "__main__":
    create_base_all_profiles_cmd()
