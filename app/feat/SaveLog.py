import logging

logging.basicConfig(
    filename="log/bot.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def log(message):
    try:
        logger.info(
            f"Message from {message.from_user.first_name}: {message.text} {sys.version_info}"
        )
    except Exception as e:
        logger.error(f"Error logging message: {e}")
