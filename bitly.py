import bitlyshortener
from bitlyshortener import Shortener

def linkshorten(linkbeforeshorten):
    tokens_pool = ['90e741cf3ceec9f9eb6b87b911ae42a007d4d6d3']  # Use your own.
    shortener = Shortener(tokens=tokens_pool, max_cache_size=8192)

    # Shorten to list

    urls = [linkbeforeshorten]
    return (shortener.shorten_urls(urls))
