from pathlib import Path

def create_local_optimization_file():
    local_file = Path(__file__).resolve().parent / "local_optimization.cmd"

    if local_file.exists():
        print(f"ℹ️ File already exists: {local_file}")
        return

    header = r"""@echo off
:: === Local Optimization Script ===
:: Auto-elevate if not run as admin
>nul 2>&1 net session
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

echo [LOCAL] Applying local user optimizations...
"""
    with open(local_file, "w", encoding="utf-8") as f:
        f.write(header)

    print(f"✅ Created file: {local_file}")

def add_local_optimizations():
    local_file = Path(__file__).resolve().parent / "local_optimization.cmd"

    if not local_file.exists():
        print(f"❌ Cannot append: File does not exist. Run create_local_optimization_file() first.")
        return

    optimizations_block = r"""

:: === HKCU Local telemetry and feedback disable ===
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f > NUL 2>&1
reg add "HKCU\Software\Microsoft\Siuf\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f > NUL 2>&1
reg add "HKCU\Software\Microsoft\Siuf\Rules" /v PeriodInDays /t REG_DWORD /d 0 /f > NUL 2>&1
reg add "HKCU\Software\Policies\Microsoft\Assistance\Client\1.0" /v "NoExplicitFeedback" /t REG_DWORD /d 1 /f > NUL 2>&1

:: Optional Office telemetry settings
reg add "HKCU\SOFTWARE\Microsoft\Office\Common\ClientTelemetry" /v "DisableTelemetry" /t REG_DWORD /d 1 /f > NUL 2>&1
reg add "HKCU\SOFTWARE\Microsoft\Office\Common\ClientTelemetry" /v "VerboseLogging" /t REG_DWORD /d 0 /f > NUL 2>&1

:: Disable Windows Media Player usage tracking
reg add "HKCU\SOFTWARE\Microsoft\MediaPlayer\Preferences" /v "UsageTracking" /t REG_DWORD /d 0 /f > NUL 2>&1

echo [OK] Local user optimizations applied.
"""
    with open(local_file, "a", encoding="utf-8") as f:
        f.write(optimizations_block)

    print(f"✅ Appended local optimizations to: {local_file}")

def add_remove_telemetry_global(cmd_file_path: Path):
    telemetry_block = r"""

:: === Global telemetry & tracking disable ===
echo [GLOBAL] Disabling telemetry services and tasks...

sc stop DiagTrack > NUL 2>&1
sc config DiagTrack start= disabled > NUL 2>&1
sc stop dmwappushservice > NUL 2>&1
sc config dmwappushservice start= disabled > NUL 2>&1
sc config diagnosticshub.standardcollector.service start= disabled > NUL 2>&1

schtasks /change /TN "\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser" /DISABLE > NUL 2>&1
schtasks /change /TN "\Microsoft\Windows\Application Experience\ProgramDataUpdater" /DISABLE > NUL 2>&1
schtasks /change /TN "\Microsoft\Windows\Application Experience\AITAgent" /DISABLE > NUL 2>&1
schtasks /change /TN "\Microsoft\Windows\Customer Experience Improvement Program\Consolidator" /DISABLE > NUL 2>&1
schtasks /change /TN "\Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask" /DISABLE > NUL 2>&1
schtasks /change /TN "\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip" /DISABLE > NUL 2>&1

reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f > NUL 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f > NUL 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\SQMLogger" /v "Start" /t REG_DWORD /d 0 /f > NUL 2>&1

echo [OK] Global telemetry settings applied.
"""
    if not cmd_file_path.exists():
        print(f"❌ Error: File not found: {cmd_file_path}")
        return

    with open(cmd_file_path, "a", encoding="utf-8") as f:
        f.write(telemetry_block)

    print(f"✅ Appended telemetry block to: {cmd_file_path}")

# Example usage:
if __name__ == "__main__":
    create_local_optimization_file()
    add_local_optimizations()

    # Optional: add global telemetry block to another .cmd
    global_script = Path(__file__).resolve().parent / "all_profiles.cmd"
    add_remove_telemetry_global(global_script)
