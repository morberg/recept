# Recept
Enkel receptsamling i markdown-format. Varje katalog är en egen kategori. Varje fil i en katalog är ett recept.

Checka ut en lokal kopia med:

    git clone https://github.com/morberg/recept.git

## Webbversion
Om man i "Settings" för github-projektet slår på GitHub Pages kan recepten automatiskt publiceras.
Det är påslaget för detta repository  och du hittar det på https://morberg.github.io/recept/ .

Filen `index.md` behöver genereras för att få en innehållsförteckning. Detta sker automatiskt med github actions när du checkar in till github.

Vill du generera `index.md` på din lokala maskin använder du `create-index.py` såhär:

    ./create-index.py > index.md
    git commit -am 'Uppdatera index'
    git push

## Utskriftsversion

Med `mdbook` går det att få till en version för utskrift. Installera `mdbook`:

```bash
brew install mdbook
```

Skapa en ny katalog, gå dit och initiera en ny bok. Någon .gitignore behövs inte. Ge boken titeln *Morbergs receptsamling*.

```bash
mdbook init
cd src
rm *
git clone https://github.com/morberg/recept.git .
./create-SUMMARY.py
cd ..
mv src/theme/ .
mdbook build
mdbook serve --open
```

Skriv ut genom att trycka på skrivarikonen uppe till höger.