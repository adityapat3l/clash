import logging
import timber
import config

timber_handler = timber.TimberHandler(source_id=config.TIMBER_SOURCE_ID, api_key=config.TIMBER_API_KEY)
logger = logging.getLogger(__name__)
logger.addHandler(timber_handler)