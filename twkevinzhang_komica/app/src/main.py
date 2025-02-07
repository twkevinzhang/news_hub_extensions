import sys
import traceback

from flask import Flask, jsonify
from werkzeug.exceptions import InternalServerError

import extension_api_pb2 as pb2

def successful(response):
    return response.SerializeToString(), 200, {'Content-Type': 'application/x-protobuf'}

app = Flask(__name__)


@app.errorhandler(InternalServerError)
def handle_500_error(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    trace = traceback.extract_tb(exc_traceback)

    # Extract relevant information
    error_info = {
        'error': str(e),
        'type': exc_type.__name__,
        'message': str(exc_value),
        'filename': trace[-1].filename,
        'line_number': trace[-1].lineno,
        'function': trace[-1].name,
        'traceback': traceback.format_exc()
    }
    return jsonify(error_info), 500

@app.route("/ping")
def ping():
    return 'pong'

@app.route("/sites/<site_id>", methods=["GET"])
async def site(site_id):
    site = pb2.Site(
        id="1",
        icon="https://komica1.org/favicon.ico",
        name="komica1.org",
        description="A description of komica1.org",
        url="https://komica1.org"
    )
    return successful(pb2.GetSiteRes(site=site))

@app.route("/boards", methods=["GET"])
async def boards():
    boards = [
        pb2.Board(
            id="1",
            site_id="1",
            name="Board 1",
            icon="https://example.com/icon1.png",
            large_welcome_image="https://example.com/welcome1.png",
            url="https://example.com/board1",
            supported_threads_sorting=["latest", "popular"]
        ),
        pb2.Board(
            id="2",
            site_id="1",
            name="Board 2",
            icon="https://example.com/icon2.png",
            large_welcome_image="https://example.com/welcome2.png",
            url="https://example.com/board2",
            supported_threads_sorting=["latest", "popular"]
        )
    ]
    return successful(pb2.GetBoardsRes(boards=boards))

@app.route("/thread-infos", methods=["GET"])
async def thread_infos():
    thread_infos = [
        pb2.ThreadInfo(
            id="1",
            board_id="1",
            site_id="1",
            url="https://example.com/thread1",
            title="Thread 1",
            author_name="Author 1",
            created_at=1633036800,
            latest_regarding_post_created_at=1633040400,
            regarding_post_count=10,
            preview_content="This is a preview of thread 1",
            tags=["tag1", "tag2"]
        ),
        pb2.ThreadInfo(
            id="2",
            board_id="1",
            site_id="1",
            url="https://example.com/thread2",
            title="Thread 2",
            author_name="Author 2",
            created_at=1633036800,
            latest_regarding_post_created_at=1633040400,
            regarding_post_count=5,
            preview_content="This is a preview of thread 2",
            tags=["tag3", "tag4"]
        )
    ]
    return successful(pb2.GetThreadInfosRes(threadInfos=thread_infos))

@app.route("/threads/<thread_id>", methods=["GET"])
async def thread(thread_id):
    thread = pb2.Thread(
        id=thread_id,
        site_id="1",
        board_id="1",
        url=f"https://example.com/thread{thread_id}",
        latest_regarding_post_created_at=1633040400,
        regarding_post_count=10,
        tags=["tag1", "tag2"],
        original_post=pb2.Post(
            id="1",
            thread_id=thread_id,
            board_id="1",
            site_id="1",
            authorId="author1",
            author_name="Author 1",
            content="This is the original post content",
            created_at=1633036800,
            title="Original Post Title",
            like=100,
            dislike=10,
            comments=20,
            contents=[
                pb2.Paragraph(type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT, text=pb2.TextParagraph(content="This is a text paragraph"))
            ]
        )
    )
    return successful(pb2.GetThreadRes(thread=thread))

@app.route("/threads/<thread_id>/regarding_posts", methods=["GET"])
async def regarding_posts(thread_id):
    regarding_posts = [
        pb2.Post(
            id="1",
            thread_id=thread_id,
            board_id="1",
            site_id="1",
            authorId="author1",
            author_name="Author 1",
            content="This is a regarding post content",
            created_at=1633040400,
            title="Regarding Post Title",
            like=50,
            dislike=5,
            comments=10,
            contents=[
                pb2.Paragraph(type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT, text=pb2.TextParagraph(content="This is a text paragraph"))
            ]
        )
    ]
    return successful(pb2.GetRegardingPostsRes(regarding_posts=regarding_posts))

@app.route("/posts/<post_id>", methods=["GET"])
async def post(post_id):
    post = pb2.Post(
        id=post_id,
        thread_id="1",
        board_id="1",
        site_id="1",
        authorId="author1",
        author_name="Author 1",
        content="This is the post content",
        created_at=1633036800,
        title="Post Title",
        like=100,
        dislike=10,
        comments=20,
        contents=[
            pb2.Paragraph(type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT, text=pb2.TextParagraph(content="This is a text paragraph"))
        ]
    )
    return successful(pb2.GetPostRes(post=post))

@app.route("/posts/<post_id>/comments", methods=["GET"])
async def comments(post_id):
    comments = [
        pb2.Comment(
            id="1",
            post_id=post_id,
            thread_id="1",
            board_id="1",
            site_id="1",
            author_id="author1",
            author_name="Author 1",
            created_at=1633040400,
            contents=[
                pb2.Paragraph(type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT, text=pb2.TextParagraph(content="This is a comment text paragraph"))
            ]
        )
    ]
    return successful(pb2.GetCommentsRes(comments=comments))

port = 55001
print("Trying to run a socket server on:", port)
app.run(port=port)
