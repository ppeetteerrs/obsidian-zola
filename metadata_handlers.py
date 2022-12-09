"""
Any function in this file is treated as a metadata handler. The function name is the metadata key.
The function takes the value of the metadata key and returns the html to be inserted into the page.
You can use existing elements or create new ones, just make sure to also create css for them.
"""
from random import choice, seed

from requests import get


def modified(date: str) -> str:
    """Converts date into html format element"""
    return f"""
            <meta property="article:modified_time" content="{date}"/>
            """


def button(text):
    return f"""
            <button class="button">{text}</button>
            """


# [![Build Status](https://img.shields.io/website?url=https%3A%2F%2Fyarden-zamir.com)](https://yarden-zamir.com)
def chips(chips_dict: dict):
    return ' '.join([_chip(key, value) for key, value in chips_dict.items()])


def _chip(key, value, should_link=True) -> str:
    key = str(key)
    value = str(value)
    if not value.startswith("http"):
        value = str(value).replace(" ", "%20")
    if not key.startswith("http"):
        key = f"https://img.shields.io/badge/{_clean_key(key)}-{_clean_url(value)}-{_random_color(key)}"
    if should_link:
        return f"[![alt text]({key})]({value})\n"
    else:
        return f"![alt text]({key})\n"


def consumed(value):
    return _chip("Consumed", value, False)


def rating(value):
    return _chip("Rating", value, False)


def _rich_link_card(url: str, type_annotation="🧠") -> str:
    try:
        resp = get(f"http://iframely.server.crestify.com/iframely?url={url}").json()
        image = [link['href'] for link in resp['links'] if
                 'thumbnail' in link['rel'] or str(link['type']).startswith("image/")][0]
        return f"""
            <div class="rich-link-card-container"><a class="rich-link-card" href="{url}" target="_blank">
                <div class="rich-link-image-container">
                    <div class="rich-link-image" style="background-image: url('{image}')">
                </div>
            </div>
            <span style="flex: auto; min-width: 0">
                <div class="rich-link-card-text">
                    <h1 class="rich-link-card-title">{resp['meta']['title'] if 'title' in resp['meta'] else _clean_url(url)}</h1>
                        <p class="rich-link-card-description">
                           {resp['meta']['description'] if 'description' in resp['meta'] else ""}
                        </p>
                    </div>
                    <p class="rich-link-href"><b>{type_annotation}</b></p> 
                </span>
            </a></div>
            """
    except: return _chip("Link 🔗", url)


def source(value):
    if value.startswith("http"):
        return _rich_link_card(value, "Source 🔍")
    return _chip("Source 🔍", value)


def aliases(list_of_aliases: list) -> str:
    # using list comprehension
    return ' '.join([_chip("Alias 🔎", alias, False) for alias in list_of_aliases])


def tags(tags_list: list) -> str:
    tags_out = ""
    for tag in tags_list:
        tags_out += f"![{tag}](https://img.shields.io/badge/{tag}-{_random_color(tag)})\n"
    return tags_out


def _clean_key(key: str) -> str:
    return key.replace(" ", "%20").replace("_", "-")


def _clean_url(url: str) -> str:
    if "/" in url:
        return url.split("/")[-1].replace("-", "--").replace(" ", "%20")
    else:
        return url.replace("-", "--").replace(" ", "%20")


def _random_color(random_seed="") -> str:
    if "/" in random_seed:
        random_seed = random_seed.split("/")[0]
    seed(random_seed)
    return choice([
        "brightgreen",
        "green",
        "yellowgreen",
        "yellow",
        "orange",
        "red",
        "blue",
        "purple",
    ])
