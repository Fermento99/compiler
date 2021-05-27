# Kompilator
## Autor: Pawel Kajanek
## Nr indeksu: 250097

---

#### Narzedzia:
- Python 3.8.5
- pip 20.0.2
- PLY 3.11

---

#### Pliki kompilatora:
- **compiler.py** (_program opakowujacy parser_)
- **parser.py** (_program eksportujacy parser_)
- **lexer.py** (_program eksportujacy lexer_)
- pomocnicze programy (_zawierajace funkcje zwracajace kod assemblera_):
  - **conditions.py**
  - **loops.py**
  - **maths.py**
  - **operations.py**
- **memory.py** (_rogram eksportujacy klase reprezntujaca pamiec maszyny_)

---

#### Uruchomienie:
Pliki *file.imp* nalezy kompilowac do kodu maszynowego za pomoca programu 'compiler.py':

`python3 compiler.py file.imp out.mr`

W przypadku, gdy nie podamy nazwy pliku wyjsciowego, kod zostanie automatycznie zapisany w pliku *out.mr*.
