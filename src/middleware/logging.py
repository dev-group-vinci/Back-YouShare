from datetime import datetime
from src.utils.logging import logger


class LoggingMiddleware(object):
    def process_request(self, req, resp):

        log_format = '[{time}] [{method}] {uri} '

        request_time = datetime.utcnow()
        request_method = req.method
        request_uri = "Route accessed: {}".format(req.path)

        log_message = log_format.format(
            time=request_time,
            method=request_method,
            uri=request_uri,
        )

        logger.info(log_message)
