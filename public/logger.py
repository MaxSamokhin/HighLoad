import logging

logging.basicConfig(filename="info.log",
                    level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")


class Logger:
    __instance = None

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            pass
        else:
            Logger.__instance = self

    @staticmethod
    def info(msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)