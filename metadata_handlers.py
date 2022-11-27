"""
Any function in this file is treated as a metadata handler. The function name is the metadata key.
The function takes the value of the metadata key and returns the html to be inserted into the page.
You can use existing elements or create new ones, just make sure to also create css for them.
"""
from random import choice, seed


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
        return f"[![alt text]({key})]({value})".strip() + "\n"
    else:
        return f"![alt text]({key})".strip() + "\n"


def consumed(value):
    return _chip("Consumed", value)


def rating(value):
    return _chip("Rating", value)


# def source(text: str) -> str:
#     return _chip("Source 🔎", text)
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
