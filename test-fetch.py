import urllib.request
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://blackpropeller.com/services/aio/'
# url = 'https://blackpropeller.com/blog/'
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
)

response = urllib.request.urlopen(req)
html = response.read().decode('utf-8', errors='replace')

soup = BeautifulSoup(html, 'html.parser')

# Try different ways to find content
post = soup.find('div', class_='post-content')
main = soup.find('main')
content_div = soup.find('div', id='content')
section = soup.find('section', class_='full-width')

print('Looking for content containers:')
print(f'  post-content: {bool(post)}')
print(f'  main: {bool(main)}')
print(f'  div#content: {bool(content_div)}')
print(f'  section.full-width: {bool(section)}')

# Use the first available container
container = post or main or content_div or section

if container:
    boxes = container.find_all('div', class_='fusion-fullwidth')
    print(f'\nFound {len(boxes)} fusion-fullwidth boxes')
    
    accordions = container.find_all('div', class_='accordian') + container.find_all('div', class_='fusion-accordian')
    print(f'Found {len(accordions)} accordions')
    
    images = container.find_all('img')
    print(f'Found {len(images)} images')
    
    if len(boxes) > 1:
        print(f'\nFirst content box (after title):')
        print(boxes[1].get('class', []))
        has_accordion = boxes[1].find('div', class_='accordian') or boxes[1].find('div', class_='fusion-accordian')
        has_images = boxes[1].find('img')
        has_content = boxes[1].find('div', class_='fusion-text') or boxes[1].find('h2')
        print(f'  Has accordion: {bool(has_accordion)}')
        print(f'  Has images: {bool(has_images)}')
        print(f'  Has content: {bool(has_content)}')
else:
    print('No content container found')

