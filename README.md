# shopcart — warsztat „Pierwsze kroki w Claude Code”

Mały sklep internetowy w Pythonie: katalog produktów, koszyk, kody rabatowe i raporty
sprzedaży. Kod jest celowo niedoskonały: ma kilka błędów i braków opisanych w
[`ISSUES.md`](ISSUES.md). Na warsztatach naprawiasz je z pomocą Claude Code.

**Zadania krok po kroku:** otwórz w przeglądarce plik [`zadania.html`](zadania.html).

## Nie pracujesz na co dzień w terminalu?

Na stronie `zadania.html` wybierz u góry tryb **Magician**. Te same zadania wykonasz
rozmową z Claude, bez wpisywania komend. Potrzebujesz tylko jednego kroku w terminalu:

1. Otwórz terminal w folderze `shopcart-kurs` (macOS: prawy przycisk na folderze →
   Usługi → Nowy terminal w folderze; Windows 11: prawy przycisk → Otwórz w terminalu).
2. Wpisz `claude` i naciśnij Enter.
3. Napisz do Claude: „Przygotuj ten projekt do pracy: utwórz środowisko .venv,
   zainstaluj zależności, skopiuj .env.example do .env i uruchom testy”.

Poniższa instrukcja jest dla trybu **Dev**.

## Wymagania

- Python 3.10 lub nowszy
- git
- Claude Code (`claude --version` powinno wypisać numer wersji)
- konto Claude (Pro, Max, Team, Enterprise) albo klucz API z Claude Console

## Przygotowanie (5 minut)

macOS / Linux / WSL:

```bash
cd shopcart-kurs
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
pytest
```

Windows (PowerShell):

```powershell
cd shopcart-kurs
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
copy .env.example .env
pytest
```

Na końcu powinno pojawić się `16 passed`. Uruchamiaj `claude` zawsze z aktywnym
środowiskiem `.venv`, wtedy Claude ma dostęp do tych samych narzędzi co Ty.

## Struktura

```text
src/shopcart/      kod aplikacji
  catalog.py       katalog produktów (data/products.json)
  cart.py          koszyk
  discounts.py     kody rabatowe
  pricing.py       VAT i formatowanie kwot
  reports.py       raporty sprzedaży (data/orders.csv)
  cli.py           wiersz poleceń: python -m shopcart ...
tests/             testy pytest
data/              dane przykładowe
ISSUES.md          zgłoszenia do rozwiązania na warsztatach
warsztat/szablony  gotowe pliki do ćwiczeń z hookami
zadania.html       interaktywna lista zadań
```

## Szybki test

```bash
python -m shopcart catalog
python -m shopcart cart --add KUB-001:2 --code LATO10
python -m shopcart report
```
