import logging
from concurrent import futures
from logging.config import dictConfig

import grpc

# configure
port = 55001

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'komica.log',
            'level': logging.DEBUG,
            'formatter': 'default'
        },
    },
    'loggers': {
        # root logger
        '': {
            'level': logging.DEBUG,
            'handlers': ['file', 'console'],
        },
    }
})
logging.debug(f'__name__ "{__name__}"')
logging.debug(f'third-party lib imported')

# When called by serious_python, __name__ is "main"
if __name__ == "__main__" or __name__ == "main":
    try:
        from twkevinzhang_komica.resolver_impl import ResolverImpl
        from twkevinzhang_komica import sidecar_api_pb2_grpc as pb2_grpc

        logging.debug(f'grpc modules imported')

        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=1),
            options=[
                ('grpc.logging_verbosity', 'DEBUG'),
            ]
        )
        pb2_grpc.add_SidecarApiServicer_to_server(ResolverImpl(), server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        logging.info("gRPC server running...")
        server.wait_for_termination()
    except Exception as e:
        logging.exception(e)
