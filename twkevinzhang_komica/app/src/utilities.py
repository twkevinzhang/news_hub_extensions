def is_youtube(url: str) -> bool:
    return 'youtube.com' in url or 'youtu.be' in url

def is_image(url: str) -> bool:
    return url.endswith(('.png', '.jpg', '.jpeg', '.gif'))

def is_video(url: str) -> bool:
    return url.endswith('.webm')
