from . import komica_domain_models_pb2 as domain_pb2

def text(s: str) -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
        text=domain_pb2.TextParagraph(content=s)
    )

def new_line() -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_NEW_LINE,
        new_line=domain_pb2.NewLineParagraph(symbol="\n")
    )

def video(s: str) -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO,
        video=domain_pb2.VideoParagraph(url=s)
    )

def youtube_video(s: str) -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO,
        video=domain_pb2.VideoParagraph(url=s)
    )

def image(s: str, thumb: str) -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE,
        image=domain_pb2.ImageParagraph(raw=s, thumb=thumb)
    )

def link(s: str) -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_LINK,
        link=domain_pb2.LinkParagraph(content=s)
    )

def reply_to(id: str, preview: str) -> domain_pb2.Paragraph:
    return domain_pb2.Paragraph(
        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
        reply_to=domain_pb2.ReplyToParagraph(id=id, author_name=id, preview=preview)
    )
