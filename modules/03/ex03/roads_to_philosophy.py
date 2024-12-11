import sys

import requests
from bs4 import BeautifulSoup


def get_first_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", id="firstHeading").text.strip()

        for content in soup.find_all("div", class_="mw-parser-output"):
            for p in content.find_all("p", recursive=False):
                for link in p.find_all("a", recursive=False):
                    href = link.get("href")
                    if href and href.startswith("/wiki/") and not href.startswith("/wiki/Help:"):
                        return f"https://en.wikipedia.org{href}", title
        return None, title

    except Exception:
        return None, None


def roads_to_philosophy(search_term: str) -> None:
    base_url = "https://en.wikipedia.org/wiki/"
    visited = []
    current_url = base_url + search_term.replace(" ", "_")

    while True:
        if current_url in visited:
            print("Infinite loop")
            break

        next_url, title = get_first_link(current_url)

        if not title:
            print("It is a dead end!!")
            break
        print(title)
        visited.append(title)

        if title == "Philosophy":
            print(f"{len(visited)} roads from {visited[0]} to Philosophy !")
            break

        if not next_url:
            print("It is a dead end!!")
            break
        current_url = next_url


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [string-to-search]")
        sys.exit(1)

    search_term = sys.argv[1].strip()
    if not search_term:
        print("Search term can't be empty")
        sys.exit(1)

    roads_to_philosophy(search_term)
