import json
from pathlib import Path

def generate_rename_cmd(old_name, new_name):
    return f"""
:: === Rename Current User ===
echo Renaming current user {old_name} to {new_name}...
wmic useraccount where name="{old_name}" rename "{new_name}"
net user "{new_name}" /fullname:"{new_name}"
"""

def generate_user_cmd(username, password="Temp1234", group="Users"):
    return f"""
:: === Create User: {username} ===
echo Creating user {username}...
net user "{username}" "{password}" /add
net localgroup "{group}" "{username}" /add

:: === Trigger profile creation ===
runas /user:{username} "cmd /c echo Profile initialized for {username}"
"""

def main():
    current_script_path = Path(__file__).resolve()
    root_dir = current_script_path.parent.parent
    input_json = root_dir / "preset_config.json"
    output_cmd = current_script_path.parent / "all_profiles.cmd"

    with open(input_json, "r", encoding="utf-8") as f:
        full_config = json.load(f)

    profiles = list(full_config.get("profiles", {}).keys())

    user_cmds = ["\n:: === User Creation Block ===", "SETLOCAL"]

    if profiles:
        # Primul profil: rename
        current_user_var = "%USERNAME%"
        rename_cmd = generate_rename_cmd(old_name=current_user_var, new_name=profiles[0])
        user_cmds.append(rename_cmd.strip())

        # Restul profilurilor: create
        for username in profiles[1:]:
            cmd_block = generate_user_cmd(username)
            user_cmds.append(cmd_block.strip())

    user_cmds.append("ENDLOCAL")
    user_cmds.append("pause")

    with open(output_cmd, "a", encoding="utf-8") as f:
        f.write("\n\n".join(user_cmds) + "\n")

    print(f"✅ Utilizatorul curent a fost redenumit și ceilalți adăugați în: {output_cmd}")

if __name__ == "__main__":
    main()
