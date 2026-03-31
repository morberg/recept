# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "recipe-scrapers",
#     "typer",
# ]
# ///

from __future__ import annotations

import json
import os
import re
from urllib.request import Request, urlopen

import typer
from recipe_scrapers import scrape_html

SOURCE_DIR = "source"

# Map English yield words to Swedish
YIELD_TRANSLATIONS = {
    "servings": "portioner",
    "serving": "portion",
    "pieces": "stycken",
    "piece": "stycke",
    "loaf": "limpa",
    "loaves": "limpor",
}


def get_categories() -> list[str]:
    """Return sorted list of category subdirectories under source/."""
    categories = []
    for entry in sorted(os.listdir(SOURCE_DIR)):
        path = os.path.join(SOURCE_DIR, entry)
        if os.path.isdir(path) and not entry.startswith("."):
            categories.append(entry)
    return categories


def prompt_category(categories: list[str]) -> str:
    """Present numbered list of categories and prompt user to choose."""
    typer.echo("Välj kategori:\n")
    for i, cat in enumerate(categories, 1):
        typer.echo(f"  {i}. {cat}")
    typer.echo()
    choice = typer.prompt("Nummer", type=int)
    if choice < 1 or choice > len(categories):
        typer.echo("Ogiltigt val.", err=True)
        raise typer.Exit(1)
    return categories[choice - 1]


def title_to_filename(title: str) -> str:
    """Convert a recipe title to a kebab-case filename.

    Preserves Swedish characters. Example:
        'Grönpepparsås' -> 'grönpepparsås.md'
        'Bakade betor med brynt hasselnöts- och misosmör' ->
            'bakade-betor-med-brynt-hasselnöts--och-misosmör.md'
    """
    name = title.lower().strip()
    # Replace whitespace with hyphens
    name = re.sub(r"\s+", "-", name)
    # Remove characters that aren't alphanumeric, hyphens, or Swedish letters
    name = re.sub(r"[^\w\-]", "", name, flags=re.UNICODE)
    # Collapse multiple hyphens
    name = re.sub(r"-{2,}", "-", name)
    name = name.strip("-")
    return f"{name}.md"


def clean_purpose(purpose: str) -> str:
    """Clean up ingredient group purpose/heading.

    Removes trailing colons, 'För', 'Till' prefixes etc.
    """
    purpose = purpose.strip()
    # Remove trailing colon
    purpose = purpose.rstrip(":")
    # Remove common Swedish prefixes like "Till " or "För "
    purpose = re.sub(r"^(Till|För)\s+", "", purpose, flags=re.IGNORECASE)
    return purpose


def translate_yields(yields: str) -> str:
    """Translate English yield words to Swedish.

    Also appends 'portioner' if yields is a bare number.
    """
    result = yields.strip()
    # If yields is just a number, append 'portioner'
    if re.fullmatch(r"\d+", result):
        return f"{result} portioner"
    for eng, swe in YIELD_TRANSLATIONS.items():
        result = re.sub(rf"\b{eng}\b", swe, result, flags=re.IGNORECASE)
    return result


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces and strip leading/trailing whitespace."""
    return re.sub(r"  +", " ", text).strip()


def looks_like_heading(item: str) -> bool:
    """Check if an ingredient item looks like a group heading rather than an ingredient.

    Heuristic: group headings are short, start with uppercase, and contain no digits.
    """
    return (
        bool(item)
        and item[0].isupper()
        and not re.search(r"\d", item)
        and len(item.split()) <= 3
        and "," not in item
        and len(item) <= 30
    )


def detect_groups_from_flat_list(
    ingredients: list[str],
) -> list[tuple[str | None, list[str]]]:
    """Detect ingredient group headings in a flat ingredient list.

    When recipe-scrapers doesn't support ingredient_groups() for a site,
    group headings end up as regular items in the ingredient list. This
    function tries to separate them back out using heuristics.

    Returns list of (heading_or_None, [ingredients]) tuples.
    """
    groups: list[tuple[str | None, list[str]]] = []
    current_heading: str | None = None
    current_items: list[str] = []

    for item in ingredients:
        if looks_like_heading(item):
            if current_items:
                groups.append((current_heading, current_items))
                current_heading = item
                current_items = []
            elif current_heading is not None:
                # Previous "heading" had no items — it was actually an ingredient.
                # Push it back to the previous group.
                if groups:
                    groups[-1][1].append(current_heading)
                else:
                    groups.append((None, [current_heading]))
                current_heading = item
            else:
                current_heading = item
        else:
            current_items.append(item)

    # Handle remaining items
    if current_items:
        groups.append((current_heading, current_items))
    elif current_heading:
        if groups:
            groups[-1][1].append(current_heading)
        else:
            groups.append((None, [current_heading]))

    return groups


def format_recipe(scraper) -> str:
    """Format scraped recipe data as markdown matching project conventions."""
    lines: list[str] = []

    # Title
    lines.append(f"# {scraper.title()}")
    lines.append("")

    # Servings
    try:
        yields = scraper.yields()
        if yields:
            lines.append(f"## {translate_yields(yields)}")
            lines.append("")
    except Exception:
        pass

    # Ingredients (with optional groups)
    try:
        groups = scraper.ingredient_groups()
    except Exception:
        groups = None

    has_groups = groups and (
        len(groups) > 1 or (len(groups) == 1 and groups[0].purpose)
    )

    if not has_groups:
        # Scraper didn't detect groups — try heuristic detection from flat list
        try:
            ingredients = scraper.ingredients()
        except Exception:
            ingredients = []
        detected = detect_groups_from_flat_list(ingredients)
        if len(detected) > 1 or (len(detected) == 1 and detected[0][0]):
            has_groups = True
            # Convert to same format we use below
            groups = detected

    lines.append("::: columns")
    lines.append("")

    if has_groups and groups:
        for group in groups:
            if isinstance(group, tuple):
                heading, ingredients = group
                if heading:
                    lines.append(f"## {clean_purpose(heading)}")
                    lines.append("")
                for ingredient in ingredients:
                    lines.append(f"- {normalize_whitespace(ingredient)}")
                lines.append("")
            else:
                # IngredientGroup from recipe-scrapers
                if group.purpose:
                    purpose = clean_purpose(group.purpose)
                    lines.append(f"## {purpose}")
                    lines.append("")
                for ingredient in group.ingredients:
                    lines.append(f"- {normalize_whitespace(ingredient)}")
                lines.append("")
    else:
        # Flat ingredient list
        try:
            ingredients = scraper.ingredients()
        except Exception:
            ingredients = []
        for ingredient in ingredients:
            lines.append(f"- {normalize_whitespace(ingredient)}")
        lines.append("")

    lines.append(":::")
    lines.append("")

    # Instructions as prose paragraphs
    try:
        instructions = scraper.instructions()
    except Exception:
        instructions = ""

    if instructions:
        # Split on newlines — recipe-scrapers typically separates steps with \n
        steps = [s.strip() for s in instructions.split("\n") if s.strip()]
        # Remove leading step numbers like "1. " or "1) "
        cleaned_steps = []
        for step in steps:
            step = re.sub(r"^\d+[\.\)]\s*", "", step)
            cleaned_steps.append(step)
        lines.append("\n\n".join(cleaned_steps))
        lines.append("")

    return "\n".join(lines)


def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL.

    Uses a Googlebot user agent to get pre-rendered HTML from SPAs
    that serve JSON-LD to crawlers.
    """
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; "
            "+http://www.google.com/bot.html)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


class JsonLdScraper:
    """Fallback scraper using JSON-LD schema.org/Recipe data embedded in HTML."""

    def __init__(self, html: str):
        self._recipe = self._extract_recipe(html)

    @staticmethod
    def _extract_recipe(html: str) -> dict:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
            except (json.JSONDecodeError, TypeError):
                continue
            recipe = JsonLdScraper._find_recipe(data)
            if recipe:
                return recipe
        raise ValueError("Ingen schema.org/Recipe data hittades på sidan")

    @staticmethod
    def _find_recipe(data) -> dict | None:
        if isinstance(data, list):
            for item in data:
                result = JsonLdScraper._find_recipe(item)
                if result:
                    return result
        elif isinstance(data, dict):
            schema_type = data.get("@type", "")
            if isinstance(schema_type, list):
                types = schema_type
            else:
                types = [schema_type]
            if "Recipe" in types:
                return data
            # Check @graph
            if "@graph" in data:
                return JsonLdScraper._find_recipe(data["@graph"])
        return None

    def title(self) -> str:
        return self._recipe.get("name", "")

    def yields(self) -> str:
        y = self._recipe.get("recipeYield", "")
        if isinstance(y, list):
            return y[0] if y else ""
        return str(y)

    def ingredients(self) -> list[str]:
        return self._recipe.get("recipeIngredient", [])

    def ingredient_groups(self):
        return []

    def instructions(self) -> str:
        instr = self._recipe.get("recipeInstructions", [])
        if isinstance(instr, str):
            return instr
        steps = []
        for item in instr:
            if isinstance(item, str):
                steps.append(item)
            elif isinstance(item, dict):
                if item.get("@type") == "HowToSection":
                    for sub in item.get("itemListElement", []):
                        if isinstance(sub, dict):
                            steps.append(sub.get("text", ""))
                        elif isinstance(sub, str):
                            steps.append(sub)
                else:
                    steps.append(item.get("text", ""))
        return "\n".join(s for s in steps if s)


app = typer.Typer()


@app.command()
def main(
    url: str = typer.Argument(help="URL till receptsida"),
    stdout: bool = typer.Option(
        False, "--stdout", help="Skriv till stdout istället för fil"
    ),
):
    """Importera recept från en webbsida och spara som markdown eller skriv till stdout."""
    typer.echo(f"Hämtar recept från {url} ...", err=True)

    try:
        html = fetch_html(url)
    except Exception as e:
        typer.echo(f"Kunde inte hämta sidan: {e}", err=True)
        raise typer.Exit(1)

    try:
        scraper = scrape_html(html, org_url=url)
    except Exception:
        try:
            scraper = JsonLdScraper(html)
            typer.echo("(Använde JSON-LD fallback)", err=True)
        except Exception as e:
            typer.echo(f"Kunde inte tolka receptet: {e}", err=True)
            raise typer.Exit(1)

    title = scraper.title()
    typer.echo(f"Hittade recept: {title}\n", err=True)

    # Generate markdown
    markdown = format_recipe(scraper)

    if stdout:
        # Output to stdout
        typer.echo(markdown)
    else:
        # Choose category and write file
        categories = get_categories()
        category = prompt_category(categories)

        # Write file
        filename = title_to_filename(title)
        filepath = os.path.join(SOURCE_DIR, category, filename)

        if os.path.exists(filepath):
            typer.echo(f"Filen finns redan: {filepath}", err=True)
            raise typer.Exit(1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown)

        typer.echo(f"\nSparat: {filepath}", err=True)


if __name__ == "__main__":
    app()
