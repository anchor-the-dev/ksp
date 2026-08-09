import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path("~/.config/ksp").expanduser()
        self.config_path = self.config_dir / "config.json"

    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.token = self.config.get("token")
        self.folder = Path(self.config.get("folder")).expanduser()
        self.template_folder = Path(self.config.get("template_folder")).expanduser()
                
    def generate_config(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.def_config = {
        "folder": "~/ksp",
        "template_folder": "~/.config/ksp/template/"}
        
        with open(self.config_path, "w") as f:
            json.dump(self.def_config, f, indent=2, ensure_ascii=False)

        self.load_config()
        self.template_folder.mkdir(parents=True, exist_ok=True)
        with open(self.template_folder/"main.py","w") as f:
            f.write("""import sys\n\nraw = [x.strip() for x in sys.stdin]\nprint(raw)""")

    



config = Config()
config.load_config()
print(config.folder)
