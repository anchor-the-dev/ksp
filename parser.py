import sys
import shutil
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import subprocess
from ksp import Config



class Parser:
    def __init__(self, url=None):
        if not url is None:
            self.url = url
            
            self.info = {
                    "kategorie": url.replace("https://ksp.mff.cuni.cz/","")[0].lower(),
                    "rocnik": int(f"{url[32]}{url[33]}"),
                    "zadani": int(url[41]) }
        self.config = Config()
        self.config.load_config()
    

    def download(self):
        """
        download self.url 
        and 
        parse its data into variables:
            self.raw raw request
            self.names  [taskid] names of tasks (Odchycení zpráv)
            self.odkazy [taskid] id of a task (task-38-Z1-1)
            self.zadani [taskid] assigment (HTML, no examples)
            self.zadani_text [taskid] assigment (raw text, no examples)
            self.zelnacka [taskid] BeautifulSoup object of assigment
            self.polivka BeautifulSoup object of entire page
            self.uk_vstup [taskid] ukázkový vstup
            self.uk_vystup [taskid] ukázkový výstup
        """
        cache_file = self.config.cache / f"{self.info['rocnik']}-{self.info['kategorie']}{self.info['zadani']}.html"
        
        if cache_file.exists():
            self.html = cache_file.read_text(encoding="utf-8")
        else:
            self.raw = requests.get(self.url)
            self.raw.raise_for_status()
            self.html = self.raw.text
            cache_file.write_text(self.html, encoding="utf-8")
        
        self.polivka = BeautifulSoup(self.html, 'html.parser')
         
        ul = self.polivka.find("ul", class_="tasks")
        li_raw  = [x.text.strip() for x in ul.select("li a")]
        self.names = [i.split(":")[1].strip() for i in li_raw ]
        self.odkazy = [f"task-{i.split(":")[0].strip()}" for i in li_raw ]
             
        z = []    
        self.zadani = []
        self.zelnacka = []
        self.uk_vstup = []
        self.uk_vystup = []
        for c,i in enumerate(self.odkazy):
            z.append([])
            x = self.polivka.find("h3", id=i)
            e = x.find_next("hr")
             
             
            for i in e.find_all_next():
                if i.name == "hr" or i.name == "h3":
                    break
                else:
                    if i.name:
                        z[c].append(str(i))
        
        for i in range(len(z)):
            self.zelnacka.append(BeautifulSoup("\n".join(z[i]),"html.parser"))
        
        for soup in self.zelnacka:
            zadani_parts = []
            for el in soup.children:
                if el.name == "div" and "leftfloat" in el.get("class", []):
                    break
                if el.name:
                    zadani_parts.append(str(el))
            self.zadani.append("\n".join(zadani_parts))
        
        self.zadani_text = [BeautifulSoup(x, "html.parser").get_text() for x in self.zadani]
         
        for i in self.zelnacka:
            k = i.find("div",class_="leftfloat")
            if not k is None:
                self.uk_vstup.append(k.find("pre").text)
            else:
                self.uk_vstup.append(None)
            
            j = i.find("div", class_="rightfloat")
            if not j is None:
                self.uk_vystup.append(j.find("pre").text)
            else:
                self.uk_vystup.append(None)

    def create_folders(self):
        base = self.config.folder / str(self.info["rocnik"]) / self.info["kategorie"] / str(self.info["zadani"])
        
        for i in range(len(self.names)):
            task_folder = base / str(i + 1)
            if not task_folder.exists():
                shutil.copytree(self.config.template_folder, task_folder)
            
            (task_folder / "zadani.txt").write_text(self.zadani_text[i], encoding="utf-8")
            
            if self.uk_vstup[i] is not None:
                (task_folder / "00.in").write_text(self.uk_vstup[i], encoding="utf-8")
            
            if self.uk_vystup[i] is not None:
                (task_folder / "00.out").write_text(self.uk_vystup[i], encoding="utf-8")
            
            if not (base / ".git").exists():
                subprocess.run(["git", "init"], cwd=base, capture_output=True)

parser = Parser(f"https://ksp.mff.cuni.cz/h/ulohy/38/zadani1.html")
parser.download()
parser.create_folders()




breakpoint()
