import requests
import re
import os
from bs4 import BeautifulSoup


def get_latest():
    link = 'https://genoanime.com/'
    # regex = r"<ul>\s*\n<li>.*<\/li><\/ul>\s*\n<h5><a\s+href=[\"'](?P<link>.*?)[\"']>(?P<title>.*?)\s+Episode\s+(?P<episode>\d+)<\/a><\/h5>"

    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')

    row = soup.select_one('#container > section.product.spad > div > div > div > div > div:nth-child(4)')

    h5s = row.select('.product__item__text > h5')

    return [
        [
            x.find('a')['href'],
            *re.findall(r"(.*?)\sEpisode\s(\d+)", x.text)[0]
        ]
        for x in h5s
    ]  # noqa


def generate_rss():
    rss = f"""
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
<title>GenoAnime - RSS Feed</title>
<link>https://github.com/ArjixGamer/anime-rss</link>
<description>A simple RSS feed for genoanime!</description>
"""

    for item in get_latest():
        rss += """
<item>
    <title>{}</title>
    <link>{}</link>
    <description>{}</description>
</item>
""".format(f"{item[1]} - Episode {item[2]}", "https://genoanime.com" + item[0][1:], f"Episode {item[2]} of {item[1]} is out!")

    rss += '\n</channel>\n</rss>'
    return rss


try:
    filename = f'./genoanime/genoanime-rss.xml'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        f.write(generate_rss().strip())
except:
    print('GenoAnime failed.')