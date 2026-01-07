from . import extension_api_pb2 as pb2
from .domain import pkg_name


def list():
    # 目前先實作 Top50 的版面
    return [
        pb2.Board(
            pkg_name=pkg_name,
            id="gita/00b",
            site_id="1",
            name="綜合",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gita.komica1.org/00b/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/79",
            site_id="1",
            name="新番捏他",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/79/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/42",
            site_id="1",
            name="四格",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/42/index.html",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/19",
            site_id="1",
            name="女性角色",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/19/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/38",
            site_id="1",
            name="男性角色",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/38/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/78",
            site_id="1",
            name="新番實況",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/78/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="atri/12",
            site_id="1",
            name="歡樂惡搞",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://atri.komica1.org/12/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="atri/23",
            site_id="1",
            name="GIF/WebM",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://atri.komica1.org/23/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="atri/67",
            site_id="1",
            name="政治",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://atri.komica1.org/67/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/09",
            site_id="1",
            name="模型",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/09/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/15",
            site_id="1",
            name="蘿蔔",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/15/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_12",
        #     site_id="1",
        #     name="影視",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://www.akraft.net/service/66a6eca2bfccee3f04a52bc4",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="atri/61",
            site_id="1",
            name="鋼普拉",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://atri.komica1.org/61/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="iris/72",
            site_id="1",
            name="Figure/GK",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://iris.komica1.org/72/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/17",
            site_id="1",
            name="軍武",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/17/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/13",
            site_id="1",
            name="特攝",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/13/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="sora/69",
            site_id="1",
            name="短片2",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://sora.komica1.org/69/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_18",
        #     site_id="1",
        #     name="TYPE-MOON",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="http://gzone-anime.info/UnitedSites/TypeMoon/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/74",
            site_id="1",
            name="Vtuber",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/74/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/73",
            site_id="1",
            name="遊戲王",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/73/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="gaia/60",
            site_id="1",
            name="奇幻/科幻",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://gaia.komica1.org/60/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="sora/81",
            site_id="1",
            name="漫畫",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://sora.komica1.org/81/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="sora/16",
            site_id="1",
            name="寫真",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://sora.komica1.org/16/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="58",
        #     site_id="1",
        #     name="飲食",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://grea.komica1.org/58/index.htm?",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="iris/64",
            site_id="1",
            name="掛圖",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://iris.komica1.org/64/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/57",
            site_id="1",
            name="中性角色",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/57/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="sora/80",
            site_id="1",
            name="動畫",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://sora.komica1.org/80/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_28",
        #     site_id="1",
        #     name="碧藍幻想",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://2cat.org/~granblue/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/25",
            site_id="1",
            name="新聞",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/25/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/27",
            site_id="1",
            name="遊戲速報",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/27/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="iris/35",
            site_id="1",
            name="小說",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://iris.komica1.org/35/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_32",
        #     site_id="1",
        #     name="手機遊戲",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://2cat.org/~handheld/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        # pb2.Board(
        #     id="komica_33",
        #     site_id="1",
        #     name="人外",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://komica.dbfoxtw.me/jingai/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        # pb2.Board(
        #     id="komica_34",
        #     site_id="1",
        #     name="AGA",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://secilia.zawarudo.org/alicegearaegis/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/52",
            site_id="1",
            name="網路遊戲",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/52/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/46",
            site_id="1",
            name="布袋戲",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/46/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/37",
            site_id="1",
            name="電腦/消費電子",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/37/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_38",
        #     site_id="1",
        #     name="萌",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://2cat.komica1.org/~kirur/img2/index.htm",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        # pb2.Board(
        #     id="komica_39",
        #     site_id="1",
        #     name="少女前線",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://secilia.zawarudo.org/gf/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        # pb2.Board(
        #     id="komica_40",
        #     site_id="1",
        #     name="網頁遊戲",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://2cat.org/~webgame/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        # pb2.Board(
        #     id="komica_41",
        #     site_id="1",
        #     name="格鬥遊戲",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://komica.yucie.net/fight/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        # pb2.Board(
        #     id="komica_42",
        #     site_id="1",
        #     name="艦隊收藏",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="http://acgspace.wsfun.com/kancolle/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/30",
            site_id="1",
            name="塗鴉王國",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/30/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_44",
        #     site_id="1",
        #     name="車",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="https://warehouse-no-99.neocities.org/all-car/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/36",
            site_id="1",
            name="擬人化",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/36/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/49",
            site_id="1",
            name="體育",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/49/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/33",
            site_id="1",
            name="高解析度",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/33/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/10",
            site_id="1",
            name="紙牌",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/10/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
        # pb2.Board(
        #     id="komica_49",
        #     site_id="1",
        #     name="祭典",
        #     icon="https://komica1.org/favicon.ico",
        #     large_welcome_image="",
        #     url="http://rthost.win/sd/",
        #     supported_threads_sorting=["latest_replied"]
        # ),
        pb2.Board(
            pkg_name=pkg_name,
            id="grea/62",
            site_id="1",
            name="氣象",
            icon="https://komica1.org/favicon.ico",
            large_welcome_image="",
            url="https://grea.komica1.org/62/index.htm",
            supported_threads_sorting=["latest_replied"]
        ),
    ]

def get(id: str):
    return next(b for b in list() if b.id == id)
