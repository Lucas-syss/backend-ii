import threading
import requests

urls = [
    "https://httpbin.org/delay/2",
    "https://httpbin.org/get",
    "https://example.com",
    "https://jsonplaceholder.typicode.com/posts"
]

def scrape(url):
    print(f"[START] {url}")
    try:
        response = requests.get(url, timeout=5)
        print(f"[DONE] {url} -> {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {url} -> {e}")

threads = []

for url in urls:
    t = threading.Thread(target=scrape, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Scraping is donee!")