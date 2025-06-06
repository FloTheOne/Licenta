class ProjectContext:
    def __init__(self, profile_names=None):
        self.profile_names = profile_names or []
        self.data = {
            name: {
                "folders": [],
                "apps": {},
                "optimizations": []
            } for name in self.profile_names
        }
        self.apps_structure = []  # Nou: structură globală de directoare pentru aplicații
        self.apps_global = {}     # Nou: apps globale (app_name → path)

    def set_folders(self, profile, folders):
        if profile in self.data:
            self.data[profile]["folders"] = folders

    def set_apps(self, profile, apps_dict):
        if profile in self.data:
            self.data[profile]["apps"] = apps_dict

    def set_optimizations(self, profile, optimizations_list):
        if profile in self.data:
            self.data[profile]["optimizations"] = optimizations_list

    def set_apps_structure(self, folder_structure):
        self.apps_structure = folder_structure

    def set_apps_global(self, apps_dict):
        self.apps_global = apps_dict

    def get_apps_structure(self):
        return self.apps_structure

    def get_apps_global(self):
        return self.apps_global

    def get_profile_data(self, profile):
        return self.data.get(profile, {})

    def get_all(self):
        return self.data
