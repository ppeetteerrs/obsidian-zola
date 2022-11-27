"""
Any function in this file is treated as a metadata handler. The function name is the metadata key.
The function takes the value of the metadata key and returns the html to be inserted into the page.
You can use existing elements or create new ones, just make sure to also create css for them.
"""


def modified(date: str) -> str:
    """Converts date into html format element"""
    return f"""
            <meta property="article:modified_time" content="{date}"/>
            """


def button(text):
    return f"""
            <button class="button">{text}</button>
            """
