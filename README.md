# psi-02 - Vícevláknový TCP server

## Spuštění
<code>python main.py {port}</code>

tj. například <code>python main.py 8888</code>
V případě, že port není uveden, použije se základní port 80.

## Detaily implementace
Server je napsán v Pythonu s využitím wrapperu okolo C-socketů, tedy používá metody
podobné jako jsou v C: socket(), bind(), listen(), accept(). Pro každé příchozí spojení
vytvoří nové vlákno, které má za úkol jeho obsluhu.

Ve smyčce se čtou data z navázaného TCP spojení, pokud v timeoutu (ve výchozím nastavení 1 s)
žádná další data nepřijdou, zahájí se zpracování. Nejprve se provede parsování HTTP requestu,
zkontroluje se, zda se strukturou jedná o HTTP request s metodou GET a jako odpověď serveru
se vrátí validní HTTP Response obsahující zprávu IT WORKS, požadovanou cestu a časovou značku serveru.