import sys
from bs4 import BeautifulSoup
from pathlib import Path
import requests



class Parser:
    def __init__(self, url=None):
        if not url is None:
            self.url = url
            
            self.info = {
                    "kategorie": url.replace("https://ksp.mff.cuni.cz/","")[0],
                    "rocnik": int(f"{url[32]}{url[33]}"),
                    "zadani": int(url[41]) }
        
    def download(self):
        """
        download self.url 
        and 
        parse its data into variables:
            self.raw raw request
            self.names  [taskid] names of tasks (Odchycení zpráv)
            self.odkazy [taskid] id of a task (task-38-Z1-1)
            self.zadani [taskid] assigment
            self.zelnacka [taskid] BeautifulSoup object of assigment
            self.polivka BuautifulSoup object of entire page
            self.uk_vstup [taskid] ukázkový vstup
            self.uk_vystup [taskid] ukázkový výstup
        """
        self.raw = requests.get(self.url)
        self.raw.raise_for_status()
                     
        self.html = self.raw.text
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
            self.zadani.append("\n".join(z[i]))
            self.zelnacka.append(BeautifulSoup("\n".join(z[i]),"html.parser"))
         
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



parser = Parser("https://ksp.mff.cuni.cz/z/ulohy/38/zadani1.html#task-38-1-1")
parser.download()




breakpoint()
