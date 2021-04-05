import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.root.setLevel(logging.NOTSET)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d : %(message)s")
logging.basicConfig(
    filename="log/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d : %(message)s",
)

log = logging.getLogger(__name__)
if os.environ.get("ENVIRONMENT") == "LOCAL":
    log.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
