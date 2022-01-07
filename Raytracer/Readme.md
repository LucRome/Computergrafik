# Readme

Der Ordner für den Ray-Tracer

## Setup

Es wird benötigt:
- Python 3.10
- Die benötigten Bibliotheken
- VS-Code mit der Python-Erweiterung (Empfohlen)
  - Dann können die gegebenen Tasks für VS-Code verwendet werden. Allerdings muss gegebenenfalls der Python Interpreter aus dem Virtual Environment verwendet werden (`F1` -> `Python: Select Interpreter`).
  - Hierfür muss der Ordner `Computergrafik` in VSCode geöffnet werden.


1. Virtual Environment erstellen und aktivieren (idealerweies in dem Ordner `Raytracer/src`)
    - ggf. Python Modul `venv` installieren
    - Virtual Environment erstellen:
    ```
    py -m venv <Venv-Folder>
    ```
    - Aktivieren:
      - Linux:
        ```
        source <Venv-Folder>/bin/activate
        ```
      - Windows (Eingabeaufforderung):
        ```
        <Venv-Folder>/Scripts/activate.bat
        ```
2. Benötigte Python Bibliotheken installieren:

```
python3 -m pip install -r ./Raytracer/src/other_files/requirements.txt
```

3. Skript `main.py` ausführen

```
python3 ./Raytracer/src/main.py
```