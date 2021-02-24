# Recept
Enkel receptsamling i markdown-format. Varje katalog är en egen kategori. Varje fil i en katalog är ett recept.

Katalogen `Referens` är en specialkatalog som innehåller markdown-filer med tabeller. Pandoc kan inte generera tabeller
och hanteras därför separat.

Checka ut en lokal kopia med:

    git clone https://github.com/morberg/recept.git

## Ingredienslista

Listan med ingredienser har ofta ganska korta rader. Det gör att sidlayouten kan bli lite konstig. Ett sätt att råda bot
på det är att visa ingredienslistan i två kolumner. Ange `::: columns` i din markdown-fil för att påbörja ett avsnitt
med två kolumner. Avsluta avsnittet med `:::`. Formatet är [pandoc
markdown](https://pandoc.org/MANUAL.html#pandocs-markdown).

Tyvärr syns just nu dessa kommandon i HTML-varianten som genereras via Jekyll på Github pages. Om man använder pandoc
för att generera HTML blir det rätt, men då behöver man hantera publiceringen till GH pages på ett annat sätt. Här finns
utrymme för förbättring.

## Webbversion
Om man i "Settings" för github-projektet slår på GitHub Pages kan recepten automatiskt publiceras.
Det är påslaget för detta repository  och du hittar det på https://morberg.github.io/recept/ .

Filen `index.md` behöver genereras för att få en innehållsförteckning. Detta sker automatiskt med github actions när du checkar in till github.

Vill du generera `index.md` på din lokala maskin gör du det med `make index.md`.

## Utskriftsversion

Installera xelatex och vänner på din maskin med `brew cask install basiclatex`. Du behöver också `brew install pandoc`.

Sen är det bara att köra `make pdf` för att generera `receptsamling.pdf` som passar bra för utskrift.
