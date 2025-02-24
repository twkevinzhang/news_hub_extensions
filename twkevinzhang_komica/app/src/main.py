import logging
from logging.config import dictConfig
import os
from concurrent import futures
import grpc
from api_server_impl import ApiServerImpl
import extension_api_pb2_grpc as pb2_grpc

# configure
port = 55001

# logging configuration
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'komica.log',
            'level': 'DEBUG',
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi', 'file'],
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
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        pb2_grpc.add_ExtensionApiServicer_to_server(ApiServerImpl(), server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        logging.info("gRPC server running...")
        server.wait_for_termination()
    except Exception as e:
        logging.exception("crashed. Error: %s", e)
