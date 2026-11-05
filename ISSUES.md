# Zgłoszenia (issue tracker projektu)

Ten plik udaje system zgłoszeń. Każde zgłoszenie ma numer, typ i kryteria akceptacji.
Na warsztatach rozwiązujesz je po kolei z pomocą Claude Code.

---

## #1 [bug] Kody rabatowe wpisane małymi literami są odrzucane

**Zgłasza:** obsługa klienta

Klienci wpisują `lato10` albo ` LATO10 ` (ze spacją skopiowaną z maila) i dostają błąd.

```
$ python -m shopcart cart --add KUB-001 --code lato10
Błąd: lato10
```

**Kryteria akceptacji**
- `lato10`, `Lato10` i `  LATO10  ` działają tak samo jak `LATO10`
- dla nieznanego kodu komunikat błędu jest czytelny, np. `Nieznany kod rabatowy: XYZ`
- testy jednostkowe pokrywają oba przypadki

---

## #2 [bug] Kod WITAJ20 daje ujemną kwotę do zapłaty

**Zgłasza:** księgowość

```
$ python -m shopcart cart --add DLG-001 --code WITAJ20
Do zapłaty: -15,09 zł
```

**Kryteria akceptacji**
- kwota do zapłaty nigdy nie jest ujemna (minimum 0,00 zł)
- najpierw powstaje test, który ten błąd odtwarza (i nie przechodzi), potem poprawka

---

## #3 [feature] Nowy kod promocyjny `3ZA2`

**Zgłasza:** marketing

Za każde 3 sztuki tego samego produktu klient płaci za 2 (najtańsza sztuka gratis
nie ma znaczenia, bo sztuki są identyczne). Przykład: 7 kubków KUB-001 = płacisz za 5.

**Kryteria akceptacji**
- kod działa niezależnie od wielkości liter (patrz #1)
- rabat liczony per produkt, nie per koszyk
- testy dla 2, 3, 6 i 7 sztuk oraz koszyka z dwoma różnymi produktami

---

## #4 [refactor] Kwoty pieniężne na `float` → `Decimal`

**Zgłasza:** zespół

Raport pokazuje kwoty w stylu `1283.1200000000001`, a ceny w całym projekcie są
liczone na liczbach zmiennoprzecinkowych.

```
$ python -m shopcart report
Przychód łącznie: 1283.1200000000001
  2026-10-01: 129.92000000000002
```

**Kryteria akceptacji**
- wszystkie kwoty (ceny, VAT, rabaty, raporty) używają `decimal.Decimal`
- zaokrąglenie do groszy: `ROUND_HALF_UP`
- raport formatuje kwoty po polsku (`1283,12 zł`)
- wszystkie istniejące testy przechodzą (mogą wymagać dostosowania typów)

---

## #5 [feature] Raport w formacie JSON

**Zgłasza:** zespół analityki

Chcemy wczytywać raport do arkusza. Potrzebna opcja:

```
$ python -m shopcart report --format json
```

**Kryteria akceptacji**
- `--format text` (domyślnie) działa jak dotąd
- `--format json` wypisuje poprawny JSON z kluczami `orders`, `total_revenue`,
  `revenue_by_day`, `top_products`
- kwoty w JSON jako napisy z dwoma miejscami po przecinku, np. `"1283.12"`
- test sprawdzający, że wyjście da się sparsować `json.loads`

---

## #6 [chore] Brak testów dla `reports.py`

Moduł `reports.py` nie ma ani jednego testu.

**Kryteria akceptacji**
- `tests/test_reports.py` z testami dla `load_orders`, `total_revenue`,
  `revenue_by_day`, `top_products`, `render_report`
- testy używają małego pliku CSV w `tests/fixtures/`, nie `data/orders.csv`

---

## #7 [docs] README nie opisuje CLI

**Kryteria akceptacji**
- sekcja „Użycie” w README z przykładem każdej komendy (`catalog`, `search`, `cart`, `report`)
- przykłady skopiowane z prawdziwego uruchomienia, nie wymyślone
