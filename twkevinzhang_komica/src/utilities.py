from typing import MutableMapping



def is_youtube(url: str) -> bool:
    return 'youtube.com' in url or 'youtu.be' in url

def is_image(url: str) -> bool:
    return url.endswith(('.png', '.jpg', '.jpeg', '.gif'))

def is_video(url: str) -> bool:
    return url.endswith('.webm')

def is_zero(s: str | int | list | MutableMapping | None):
    if isinstance(s, str):
        return s == ""
    elif isinstance(s, int):
        return s == 0
    elif isinstance(s, list):
        return len(s) == 0
    elif isinstance(s, MutableMapping):
        return len(s.keys()) == 0
    else:
        return s is None
