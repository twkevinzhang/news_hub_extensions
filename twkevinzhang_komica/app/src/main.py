import logging
from logging.config import dictConfig
import os
from concurrent import futures
import grpc

# configure
port = 55001

# logging configuration
# print() will not be logged
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
        # grpc default logger
        'grpc': {
            'level': logging.DEBUG,
            'handlers': ['file', 'console'],
            'propagate': False,  # 防止日志消息被传递到根日志器
        },
    }
})
logging.debug(f'__name__ "{__name__}"')

# serious_python unsupported multiprocessing
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

# When called by serious_python, __name__ is "main"
if __name__ == "__main__" or __name__ == "main":
    try:
        from api_server_impl import ApiServerImpl
        import extension_api_pb2_grpc as pb2_grpc
        logging.debug(f'komica and grpc modules imported')

        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=1),
            options=[
                ('grpc.logging_verbosity', 'DEBUG'),
            ]
        )
        pb2_grpc.add_ExtensionApiServicer_to_server(ApiServerImpl(), server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        logging.info("gRPC server running...")
        server.wait_for_termination()
    except Exception as e:
        logging.exception(e)
