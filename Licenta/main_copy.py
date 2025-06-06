import tkinter as tk
from tkinter import ttk
import requests

class ChocoAppInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Chocolatey App Installer")
        self.root.geometry("800x600")
        self.app_vars = []

        self.build_ui()

    def build_ui(self):
        # Search section
        search_frame = ttk.Frame(self.root, padding=10)
        search_frame.pack(fill=tk.X)

        self.search_entry = ttk.Entry(search_frame, width=60)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        search_button = ttk.Button(search_frame, text="Search", command=self.search_apps)
        search_button.pack(side=tk.LEFT)

        # Results section
        self.result_frame = ttk.Frame(self.root, padding=10)
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_canvas = tk.Canvas(self.result_frame)
        self.scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.result_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))
        )

        self.result_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.result_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Generate script button
        script_btn = ttk.Button(self.root, text="Generate Script", command=self.generate_script)
        script_btn.pack(pady=10)

        # Output script
        self.script_output = tk.Text(self.root, height=10, wrap=tk.WORD)
        self.script_output.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

    def search_apps(self):
        query = self.search_entry.get().strip()
        if not query:
            return

        self.clear_results()
        apps = self.search_choco_packages(query)

        for app in apps:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.scrollable_frame, text=f"{app['title']} ({app['id']})", variable=var)
            checkbox.pack(anchor="w")
            self.app_vars.append((var, app["id"]))

    def clear_results(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.app_vars = []
        self.script_output.delete(1.0, tk.END)

    def generate_script(self):
        lines = [
            "Set-ExecutionPolicy Bypass -Scope Process -Force",
            "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072",
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))",
            ""
        ]
        for var, app_id in self.app_vars:
            if var.get():
                lines.append(f"choco install {app_id} -y")

        script = "\n".join(lines)
        self.script_output.delete(1.0, tk.END)
        self.script_output.insert(tk.END, script)

    def search_choco_packages(self, query, top=30):
        url = "https://community.chocolatey.org/api/v2/Search()"
        params = {
            "searchTerm": f"'{query}'",
            "$top": top,
            "$skip": 0,
            "$filter": "IsLatestVersion",
            "includePrerelease": "false",
            "targetFramework": ""
        }
        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = []
            for entry in data.get("d", {}).get("results", []):
                results.append({
                    "id": entry.get("Id", ""),
                    "title": entry.get("Title", entry.get("Id", "")),
                    "version": entry.get("Version", ""),
                    "summary": entry.get("Summary", "")
                })
            return results

        except Exception as e:
            print(f"Error: {e}")
            return []

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChocoAppInstaller(root)
    root.mainloop()
