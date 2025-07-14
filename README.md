# Recept

Enkel receptsamling i markdown-format. Alla recept ligger under katalogen `source`. Varje
underkatalog är en egen kategori. Varje fil i en katalog är ett recept.

Checka ut en lokal kopia med:

    git clone https://github.com/morberg/recept.git

## Ingredienslista

Listan med ingredienser har ofta ganska korta rader. Det gör att sidlayouten kan bli lite
konstig. Därför visar vi gärna ingredienslistan i två kolumner. Ange
`::: columns` i din markdown-fil för att påbörja ett avsnitt med två kolumner. Avsluta
avsnittet med `:::`. Formatet är [pandoc
markdown](https://pandoc.org/MANUAL.html#pandocs-markdown).

## Länkar mellan recept

Det går bra att länka mellan recept, kommer att fungera både i webb-versionen
och i PDF:en. Använd relativa länkar till den markdown-fil som har receptet och
ha inte med någon filändelse (t.ex. `[länktext](../Smått/sichuansk-chiliolja)).

## Beroenden

Installera xelatex och vänner på din maskin med t.ex. `brew install basictex`. Du behöver
också `brew install pandoc`. Senast testat med pandoc 3.2.1 och TeX Live 2024.

Slutligen behövs `brew install uv` för att köra python-koden som finns i `tools`.

## Webbversion

Om man i "Settings" för github-projektet slår på GitHub Pages kan recepten under katalogen
`docs` automatiskt publiceras. Det är påslaget för detta repository och du hittar
resultatet på <https://morberg.github.io/recept/> .

Filen `index.md` behöver genereras för att få en innehållsförteckning. Detta sker
automatiskt med github actions när du checkar in till github. Även katalogen `docs`, som
innehåller filerna för webbversionen, behöver generas. Det sker också via github actions.

Vill du generera `index.md` på din lokala maskin gör du det med `make index.md`. För
att generera docs-katalogen lokalt kör du `make jekyll`.

## Utskriftsversion

Sen är det bara att köra `make pdf` för att generera `pdf/receptsamling.pdf` som passar
bra för utskrift.
