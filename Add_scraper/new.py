from bs4 import BeautifulSoup
import re

soup = BeautifulSoup("https://www.whatmobile.com.pk/")
script = soup.find('script')
mp4 = re.compile(r"(?<=js:\s\[\')(.*)\'\]")
print(mp4.findall(script.get_text())[0])