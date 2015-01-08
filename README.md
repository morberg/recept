# Recept
Enkel receptsamling i markdown-format. Varje katalog är en egen kategori. Varje fil i en katalog är ett recept.

Checka ut en lokal kopia med:

    git clone https://github.com/morberg/recept.git

## Generera PDF
* Använd Atom som editor.
* Installera paketet `markdown-pdf`
* Ändra eventuellt typsnitt i `markdown-preview` från Helvetica Neue till Avenir
* Generera PDF inifrån editorn med Shift+Cmd+C

## Webbversion
Middleman och Franklin verkar funka smidigast och med minst handpåläggning.

Sätt upp Middleman och [Franklin](https://github.com/bryanbraun/franklin):

    % gem install middleman
    % git clone git@github.com:bryanbraun/franklin.git ~/.middleman/franklin

Skapa katalog för receptsamlingen och gå dit:

    % middleman init recept --template=franklin
    % cd recept

Lägg till följande i `Gemfile`:

    gem 'middleman-deploy', '~> 1.0.0'

Uppdatera `config.rb` med följande:

    activate :deploy do |deploy|
    deploy.method = :git
    # Optional Settings
    deploy.remote   = 'morberg.github.io' # remote name or git url, default: origin
    deploy.branch   = 'master' # default: gh-pages
    # deploy.strategy = :submodule      # commit strategy: can be :force_push or :submodule, default: :force_push
    # deploy.commit_message = 'custom-message'      # commit message (can be empty), default: Automated commit at `timestamp` by middleman-deploy `version`
    end

Avsluta med att installera alla beroenden:

    % bundle install  # Installs any franklin-specific gems.

Gå till `source`, ta bort default-filer och checka ut receptsamlingen:

    % cd source
    % rm *.md
    % git init .
    % git remote add -t \* -f origin https://github.com/morberg/recept.git
    % git checkout master
    % cd ..

Uppdatera `data/book.yml`:

    ---
    title: Receptsamling
    author: Niklas Morberg
    github_url: https://github.com/morberg.github.io
    domain: http://morberg.github.io/
    license_name: Attribution-ShareAlike
    license_url: https://creativecommons.org/licenses/by-sa/4.0
    theme: epsilon

Nu är allt uppsatt. Skapa HTML-sidorna till katalogen `build` med:

    bundle exec middleman build

Kolla på den lokalt med:

    bundle exec middleman server

och sedan

    bundle exec middleman deploy

för att publicera till http://morberg.github.io.
