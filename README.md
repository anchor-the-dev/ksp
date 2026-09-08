# ksp-client

## použití:
### stažení dependencies:
```
python3 -m .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### generování config file:

```
python3 parser.py -genconfig
```
- toto vytvoří ~/.config/ksp/config.json ~/.config/ksp/template ~/config/ksp/cache

- výchozí config
```
{
  "folder": "~/ksp",
  "template_folder": "~/.config/ksp/template/",
  "cache": "~/.config/ksp/cache"
}
```
- folder: kde se ukládá struktura ksp
- template_folder: složka ze které se kopíruje do jednotlivých úkolů
- cache: cache složka

# spuštění
```
python3 parser.py 
Zadejte url nějaké série: 
https://ksp.mff.cuni.cz/z/ulohy/37/zadani1.html#   
```
- toto vytvoří ve folder z configu tuto strukturu:


```
ksp/
    ročník/
           typ(h/z)/
                    série/
                         úloha/
                              zadani.txt (soubor se zadáním)
                              obsah template_folder (všechen obsah template_folder)
                              00.in  (pokud je úloha praktická)
                              00.out (pokud je úloha praktická)
```

