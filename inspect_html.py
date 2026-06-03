import requests
from bs4 import BeautifulSoup

url = "https://python.langchain.com/docs/introduction/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Cerca tag semantici
for tag_name in ["article", "main"]:
    tag = soup.find(tag_name)
    if tag:
        print(f"Trovato tag: {tag_name}")
        print(tag.get_text()[:500])
        print("---")
    else:
        print(f"Tag {tag_name} non trovato")