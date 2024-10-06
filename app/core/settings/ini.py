import os.path
from configparser import ConfigParser
from app.common.common import ROOT, CONFIG_NAME
from fastapi_babel import _

LOG_SECTION_NAME = 'Log'
DATABASE_SECTION_NAME = 'Psql'
FLASK_SECTION_NAME = 'Flask'
AUTH_SECTION_NAME = 'Auth'
WEBSOCKET_PORT = 'WebSocketPort'
REDIS_SECTION_NAME = 'Redis'
LIS_SECTION_NAME = 'Lis'
PATENT_SECTION_NAME = 'Patent'
FINAL_VERSION_NAME = 'FinalVersion'
TRANSLATION_SECTION_NAME = 'Translation'


class Config(object):

    def __init__(self, configini):
        self.cfgparser = ConfigParser()
        self.cfgparser.optionxform = str
        self.cfgparser.read(configini)

    def get_translation_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(TRANSLATION_SECTION_NAME):
            _meta = dict(self.cfgparser.items(TRANSLATION_SECTION_NAME))

        translation_path = _meta.get('TRANSLATION-PATH', 'D:/CygnusS/app/translation/lang')
        return translation_path

    def get_log_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(LOG_SECTION_NAME):
            _meta = dict(self.cfgparser.items(LOG_SECTION_NAME))

        log_path = _meta.get('LOG-PATH', 'None')
        log_path_user = _meta.get('USER-LOG-PATH', 'None')
        maxsize = _meta.get('MAXSIZE', 'None')
        backup_count = _meta.get('BACKUP-COUNT', 'None')

        return log_path, maxsize, backup_count, log_path_user

    def get_flask_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(FLASK_SECTION_NAME):
            _meta = dict(self.cfgparser.items(FLASK_SECTION_NAME))

        # FLASK_PORT = 5000
        # FLASK_IP = 0.0.0.0
        # FLASK_DEBUG = 1
        flask_port = int(_meta.get('FLASK_PORT', '5000'))
        flask_ip = _meta.get('FLASK_IP', '0.0.0.0')
        flask_debug = int(_meta.get('FLASK_DEBUG', '1'))
        return flask_port, flask_ip, flask_debug

    def get_psql_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(DATABASE_SECTION_NAME):
            _meta = dict(self.cfgparser.items(DATABASE_SECTION_NAME))

        """
        PG_DB_NAME = cygnus
        PG_DB_USERNAME = postgres
        PG_DB_PASSWORD = postgres
        PG_DB_IP = 127.0.0.1
        PG_DB_PORT = 5432
        """
        pg_ip = _meta.get('PG_DB_IP', '127.0.0.1')
        pg_port = _meta.get('PG_DB_PORT', 5432)
        pg_db_name = _meta.get('PG_DB_NAME', 'cygnus')
        pg_username = _meta.get('PG_DB_USERNAME', 'postgres')
        pg_password = _meta.get('PG_DB_PASSWORD', '123456')
        # pg_scheme = _meta.get('PG_DB_SCHEME', 'postgresql+asyncpg')
        pg_scheme = _meta.get('PG_DB_SCHEME', 'postgresql')

        return pg_ip, int(pg_port), pg_db_name, pg_username, pg_password, pg_scheme

    def get_auth_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(AUTH_SECTION_NAME):
            _meta = dict(self.cfgparser.items(AUTH_SECTION_NAME))

        """
        [Auth]
        JWT_ALGORITHM = HS256
        JWT_EXPIRE_SECONDS = 43200
        """
        jwt_al = _meta.get('JWT_ALGORITHM', 'HS256')
        jwt_exp = _meta.get('JWT_EXPIRE_SECONDS', '43200')
        jwt_subject = _meta.get('JWT_SUBJECT', 'xiaoying')

        return jwt_al, jwt_exp, jwt_subject

    def get_redis_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(REDIS_SECTION_NAME):
            _meta = dict(self.cfgparser.items(REDIS_SECTION_NAME))

        """
        REDIS_IP = 127.0.0.1
        REDIS_PORT = 6379
        REDIS_DB = 0
        """
        redis_ip = _meta.get('REDIS_IP', '127.0.0.1')
        redis_port = _meta.get('REDIS_PORT', '6379')
        redis_db = _meta.get('REDIS_DB', '0')
        redis_passwd = _meta.get('REDIS_PASSWD', '')

        return redis_ip, int(redis_port), redis_db, redis_passwd

    def get_lis_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(LIS_SECTION_NAME):
            _meta = dict(self.cfgparser.items(LIS_SECTION_NAME))

        """
        LIS_IP = "192.168.3.100"
        LIS_PORT = "8000"
        """
        lis_ip = _meta.get('LIS_IP', '192.168.3.100')
        lis_port = _meta.get('LIS_PORT', '8000')

        return lis_ip, lis_port

    def get_patent_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(PATENT_SECTION_NAME):
            _meta = dict(self.cfgparser.items(PATENT_SECTION_NAME))

        product_name = _meta.get('PRODUCT_NAME', '全自动学细胞形态学分析仪')
        product_series = _meta.get('PRODUCT_SERIES', 'Cygnus')
        software_name = _meta.get('SOFTWARE_NAME', 'CellaScope')
        hardware_name = _meta.get('HARDWARE_NAME', 'Cygnus-12')
        description = _meta.get('DESCRIPTION',
                                '本产品出厂前已部署配置完相关软硬件，产品可识别各类正常细胞及异常细胞。异常细胞详细分类数据仅供使用者科研参考使用。')
        attention = _meta.get('ATTENTION', '请在该类器械监管要求使用下使用本产品')
        release_num = _meta.get('RELEASE_NUM', '2023001')

        return _(product_name), product_series, software_name, hardware_name, \
               _(description), _(attention), release_num

    def get_final_version_cfg(self):

        _meta = {}
        if self.cfgparser.has_section(FINAL_VERSION_NAME):
            _meta = dict(self.cfgparser.items(FINAL_VERSION_NAME))

        software_python = _meta.get('SOFTWARE_PYTHON', 'V.1.0.0.0')
        software_ui = _meta.get('SOFTWARE_UI', 'V.1.0.0.0')
        software_go = _meta.get('SOFTWARE_GO', 'V.1.0.0.0')
        hardware = _meta.get('HARDWARE', 'V.1.0.0.0')
        ALG_white = _meta.get('ALG_WHITE', 'V.1.0.0.0')
        ALG_red = _meta.get('ALG_RED', 'V.1.0.0.0')
        ALG_PC = _meta.get('ALG_PC', 'V.1.0.0.0')
        release_num = _meta.get('RELEASE_NUM', '2024001')

        return software_python, software_ui, software_go, hardware, ALG_white, ALG_red, ALG_PC, release_num


CygnusConfig = Config(os.path.join(ROOT, CONFIG_NAME))
