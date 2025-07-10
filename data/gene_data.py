import requests
from bs4 import BeautifulSoup
import re
import wikipediaapi
import os

# Configuration
OUTPUT_FILE = "french_text_data.txt"
WIKI_PAGES = ["France", "Littérature_française", "Science", "Histoire"]  # French Wikipedia pages
LE_MONDE_URLS = [  # Example Le Monde article URLs
    "https://www.lemonde.fr/politique/article/2023/10/10/...",
    "https://www.lemonde.fr/culture/article/2023/10/05/...",
]
GUTENBERG_BOOK_IDS = [50964, 58852]  # French books on Project Gutenberg (e.g., Les Misérables)

# --- 1. Scrape French Wikipedia ---
def scrape_wikipedia():
    wiki_wiki = wikipediaapi.Wikipedia('fr')
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for page in WIKI_PAGES:
            page_py = wiki_wiki.page(page)
            if page_py.exists():
                text = re.sub(r'\n{3,}', '\n\n', page_py.text)  # Remove excessive newlines
                f.write(text + "\n\n")

# --- 2. Scrape Le Monde Articles ---
def scrape_le_monde():
    headers = {'User-Agent': 'Mozilla/5.0'}
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for url in LE_MONDE_URLS:
            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                article = soup.find('article')
                paragraphs = article.find_all('p')
                text = '\n'.join([p.get_text() for p in paragraphs])
                f.write(text + "\n\n")
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

# --- 3. Scrape Project Gutenberg (French Books) ---
def scrape_gutenberg():
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for book_id in GUTENBERG_BOOK_IDS:
            try:
                url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
                response = requests.get(url)
                response.encoding = 'utf-8'
                text = re.sub(r'\r\n', '\n', response.text)  # Normalize line breaks
                f.write(text + "\n\n")
            except Exception as e:
                print(f"Failed to scrape book {book_id}: {e}")

# --- Main ---
if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)  # Clear existing file

    print("Scraping Wikipedia...")
    scrape_wikipedia()

    print("Scraping Le Monde...")
    scrape_le_monde()

    print("Scraping Project Gutenberg...")
    scrape_gutenberg()

    print(f"Done! Data saved to {OUTPUT_FILE}")