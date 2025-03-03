import extension_api_pb2 as pb2

def text(s: str) -> pb2.Paragraph:
    return pb2.Paragraph(
        type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
        text=pb2.TextParagraph(content=s)
    )

def video(s: str, thumb: str) -> pb2.Paragraph:
    return pb2.Paragraph(
        type=pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO,
        video=pb2.VideoParagraph(url=s)
    )

def youtube_video(s: str) -> pb2.Paragraph:
    return pb2.Paragraph(
        type=pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO,
        video=pb2.VideoParagraph(url=s)
    )

def image(s: str, thumb: str) -> pb2.Paragraph:
    return pb2.Paragraph(
        type=pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE,
        image=pb2.ImageParagraph(raw=s, thumb=thumb)
    )

def link(s: str) -> pb2.Paragraph:
    return pb2.Paragraph(
        type=pb2.ParagraphType.PARAGRAPH_TYPE_LINK,
        link=pb2.LinkParagraph(content=s)
    )

def reply_to(s: str, preview: str) -> pb2.Paragraph:
    return pb2.Paragraph(
        type=pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
        reply_to=pb2.ReplyToParagraph(id=s, preview=preview)
    )
