import requests
from bs4 import BeautifulSoup
import os
import re

visited_links = set()

def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

def get_external_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if is_valid_url(href) and href not in visited_links:
            links.append(href)
            visited_links.add(href)
    
    return links

def crawl_links(url, depth=1, max_depth=2):
    if depth > max_depth:
        return

    external_links = get_external_links(url)
    for link in external_links:
        print(f"[Depth {depth}] {link}")
        crawl_links(link, depth + 1, max_depth)

def main():
    start_url = input("Enter the start URL: ").strip()
    output_choice = input("Enter '1' to print results in terminal, '2' to save to file: ").strip()

    if not is_valid_url(start_url):
        print("Invalid URL. Please enter a valid URL starting with http:// or https://")
        return

    visited_links.add(start_url)
    results = []

    def collect_links(url, depth=1, max_depth=2):
        if depth > max_depth:
            return
        external_links = get_external_links(url)
        for link in external_links:
            results.append(f"[Depth {depth}] {link}")
            collect_links(link, depth + 1, max_depth)

    collect_links(start_url)

    if output_choice == '1':
        for result in results:
            print(result)
    elif output_choice == '2':
        filename = input("Enter the filename to save results: ").strip()
        with open(filename, 'w') as file:
            for result in results:
                file.write(result + '\n')
        print(f"Results saved to {filename}")
    else:
        print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
