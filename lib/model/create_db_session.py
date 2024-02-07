from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from stringcase import snakecase
import lib.log as log
import pytest
from sqlalchemy.orm import scoped_session
import settings

logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)


def db_session(db_key):
    '''
    Creates a Session instantiated sqlalchemy engine for connection resources and establishes a transaction on that connection
    :param db_key: database config details from config/setup.yml and provides a particular db URL
    :return: session object
    '''
    db_uri = settings.get_db_uri(snakecase(db_key.lower()))

    logger.info('Obtained DB uri')
    engine = create_engine(db_uri)

    Session = scoped_session(sessionmaker(bind=engine))

    pytest.test_data.update({'db_session': Session()})
    logger.info('Started DB Session')

    settings.GLOBAL_DB_SESSION = Session()
    return settings.GLOBAL_DB_SESSION
