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

## Webbversion
Om man i "Settings" för github-projektet slår på GitHub Pages kan recepten under katalogen
`docs` automatiskt publiceras. Det är påslaget för detta repository och du hittar
resultatet på https://morberg.github.io/recept/ .

Filen `index.md` behöver genereras för att få en innehållsförteckning. Detta sker
automatiskt med github actions när du checkar in till github. Även katalogen `docs`, som
innehåller filerna för webbversionen, behöver generas. Det sker också via github actions.

Vill du generera `index.md` på din lokala maskin gör du det med `make index.md`. För
att generera docs-katalogen lokalt kör du `make jekyll`.

## Utskriftsversion

Installera xelatex och vänner på din maskin med `brew cask install basiclatex`. Du behöver
också `brew install pandoc`.

Sen är det bara att köra `make pdf` för att generera `receptsamling.pdf` som passar bra
för utskrift.
