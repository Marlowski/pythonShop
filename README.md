# Projekt richtig klonen
1. Im Startfenster von PyCharm **get from VCS** anklicken & dann das richtige repo auswählen
2. Es sollte nun ein neues Projekt angelegt worden sein, indem aber noch kein venv Ordner existiert.
3. Dafür öffnen wir: <br/>(mac): **PyCharm | Preferences | Project | Python Interpreter**<br/>(Windows): **File | Settings | Project | Python Interpreter**<br/>
4. In diesem Fenster oben rechts auf das **Zahnrad** klicken und **add** auswählen.
5. Nun die Richtige Python Version auswählen _(3.x)_ und hinzufügen.
6. Wir kehren nun ins Fenster davor zurück und klicken links auf das **plus Symbol**. Dort suchen wir nach "Django" und fügen das Packet dem Projekt hinzu.
7. Nun sollte das Programm einsatzbereit sein und mit **python manage.py runserver** zum laufen gebracht werden können.


## Eigenes Projekt richtig mit dem Repository mergen
1. Neue eigene Änderung **commiten**
2. Veränderungen im Repo mit **git pull** holen
3. Änderungen in eigenen Code übernehmen
4. Erneut **commiten** und dann **git push**