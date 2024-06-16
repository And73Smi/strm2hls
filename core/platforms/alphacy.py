import requests
from bs4 import BeautifulSoup
import re
import sys
import subprocess

def install_bs4():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])

try:
    from bs4 import BeautifulSoup
except ImportError: 
    install_bs4()
    from bs4 import BeautifulSoup

# URL of the webpage containing the wmsAuthSign
webpage_url = 'https://www.alphacyprus.com.cy/live'

# Fetch the content of the webpage
response = requests.get(webpage_url)
print(f"HTTP Status Code for webpage fetch: {response.status_code}")  # Log the status code for webpage fetch
print(f"HTTP Headers for webpage fetch: {response.headers}")  # Log the headers for webpage fetch

if response.status_code == 200:  # This will check if the HTTP request returned a successful status code
    webpage_content = response.text
else:
    raise Exception(f"Failed to fetch the webpage: {webpage_url}")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage_content, 'html.parser')

# Find the wmsAuthSign in the HTML content
wmsAuthSign = None
for script in soup.find_all('script'):
    if 'wmsAuthSign' in script.text:
        # Extract the wmsAuthSign from the script text
        match = re.search(r'wmsAuthSign=([a-zA-Z0-9%_-]+)', script.text)
        if match:
            wmsAuthSign = match.group(1)
            break

if not wmsAuthSign:
    raise Exception("wmsAuthSign not found in the webpage")

# Construct the final m3u8 URL with the wmsAuthSign
m3u8_base_url = 'https://l4.cloudskep.com/alphacyp/acy/playlist.m3u8'
final_m3u8_url = f"{m3u8_base_url}?wmsAuthSign={wmsAuthSign}=="

# Fetch the m3u8 content from the final URL
m3u8_response = requests.get(final_m3u8_url)
print(f"HTTP Status Code for m3u8 fetch: {m3u8_response.status_code}")  # Log the status code for m3u8 fetch
print(f"HTTP Headers for m3u8 fetch: {m3u8_response.headers}")  # Log the headers for m3u8 fetch

if m3u8_response.status_code == 200:
    m3u8_content = m3u8_response.text
else:
    print(f"Failed to fetch the m3u8 file: {m3u8_response.text}")  # Log the error message if m3u8 fetch failed
    raise Exception(f"Failed to fetch the m3u8 file {final_m3u8_url}")

# Save the m3u8 content to a file
with open('alphacyprus.m3u8', 'w') as file:
    file.write(m3u8_content)

print(f"The final m3u8 URL is {final_m3u8_url}")
print("The m3u8 content has been saved to alphacyprus.m3u8")
