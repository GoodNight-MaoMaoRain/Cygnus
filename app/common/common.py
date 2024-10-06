# 工程文件夹路径
# ROOT = 'app/api/engineer/log_doc'
# 配置文件名车给你
CONFIG_NAME = "cygnus.ini"

# 日志类型 质控 QC、错误 error、升级 upgrade、操作 operation
LOG_QC = "QC"
LOG_ERROR = "error"
LOG_UPGRADE = "upgrade"
LOG_OPERATION = "operation"

import os

# BASE_DIR = Path(__file__).resolve().parent.parent
"""路径配置"""
# 当前工程路径
BASE_DIR = 'app/api/engineer/log_doc'
# 工程文件夹路径
ROOT = r"D:\CygnusS\app\api\engineer\log_doc"
# 图片存储路径,后续用于docker部署挂载磁盘
IMAGE_ROOT = 'app/api/engineer/log_doc'
# go代码模块路径
GO_ROOT = r"D:\CygnusS\app\api\engineer\log_doc"
# 下位机硬件代码模块路径
HARDWARE_ROOT = 'app/api/engineer/log_doc'
# 下载文件放置路径
DOWNLOADS_PATH = r"D:\CygnusS\app\api\engineer\log_doc"
# python日志文件路径
PYTHON_LOG_PATH = os.path.join(ROOT, "logs")
# go代码模块日志文件路径
GO_LOG_PATH = os.path.join(GO_ROOT, "logs")
# 用户操作日志文件路径
PRODUCT_LOG_PATH = os.path.join(ROOT, "logs_user")
# 下位机硬件日志文件路径
HARDWARE_LOG_PATH = os.path.join(HARDWARE_ROOT, "logs")
# 版权信息存储路径
PATENT_PATH = os.path.join(ROOT, "")
# 质控模块标准图片存储路径
STANDARD_IMAGES_PATH = os.path.join(ROOT, "standard_images")
# docker_compose文件存储路径
DOCKER_COMPOSE_PATH = "/home/xiaoying/project/docker-file/docker-compose.yml"

# # 常量定义
# PYTHON_TYPE = "python"
# GO_TYPE = "go"
# PRODUCT_TYPE = "product"
# HARDWARE_TYPE = "hardware"

"""任务状态"""
ACTIVE = "Active"
WAITING = "Waiting"
PRE_SCAN = "PreScan"
SUCCESS = "Success"
FAILURE = "Failure"
SCANNING = [ACTIVE, PRE_SCAN]
WAITING_SCANNING = [ACTIVE, WAITING, PRE_SCAN]
NO_SCANNING = [SUCCESS, FAILURE]

"""任务类型"""
NORMAL_TASK = "Normal"

"""参数配置"""
# 拍摄玻片图片高
SLIDE_IMAGE_HEIGHT = 1520
# 拍摄玻片图片宽
SLIDE_IMAGE_WIDTH = 580
# 实体玻片的宽mm
SLIDE_WIDTH = 26
# 实体玻片的高mm
SLIDE_HEIGHT = 76
# 玻片盒子使用最大次数
BOX_MAX_COUNT = 1000
# 缓存任务的最大数量
CACHE_TASK_MAX_COUNT = 5
# 允许创建用户的最大数量
USER_COUNT = 10
# 允许疟疾创建的按个数扫描范围
PARASITE_LIMIT = [0, 500, 1000, 1500, 2000]
LIMIT_SCAN_CELL_MIN_COUNT = 0
# 不舒展配置
NOT_STRETCHING = True
# 系统是否为协和版本， True为协和版(注意：没有不舒展功能，所以为True时关闭不舒展配置)，False为定版
NOT_XIEHE = False
# 判断是否舒展阈值
QUALITY_COUNT = 7
# 紧急配置
IS_EMERGENCY = False
# 是否兼容长方形， True为兼容，False为正方形显示
IS_RECTANGLE = True
# 不舒展参数超过该比例进行提示
QUALITY_TIP_THRESHOLD = 0.5
# 部分细胞类别直径小于70像素丢弃
DISCARD_PX = 70
# 血小板浓度计算模块显微图片数量
PC_IMAGE_COUNT = 32
# 下位机未连接多长时间报错
HARDWARE_NO_CONNECT_TIME = 600
# 是否增强
IS_ENHANCED = True

"""玻片地图显示尺寸"""
# 玻片地图显示宽
WIDTH = 1200
# 玻片地图显示高
HEIGHT = 1200
# 玻片地图尺寸
IMAGE_REAL_SIZE = 1200
# 显微图片真实宽尺寸
IMAGE_REAL_WIDTH_SIZE = 1200
# 显微图片真实高尺寸
IMAGE_REAL_HEIGHT_SIZE = 1800
# 1024÷200×30 = 153.6 扫描大图等于多少微米
LARGE_PX_UM = 0.1536
# 扫描大图等于多少微米
IMAGE_2_UM = 132.4  # 113
# 扫描大图1微米等于多少像素
LARGE_UM_PX = IMAGE_REAL_WIDTH_SIZE / IMAGE_2_UM
# 扫描大图1微米等于多少像素
LARGE_UM_PX_temp = 11.5
# 加密加盐，字符串暂定为：xiaoying
SALT = "xiaoying"
# 添加自定义细胞类别标识符号
SELF_DEFINE_MARK = "add"
# 修改细胞类别参数列表,A修改细胞类别 B修改分裂后的细胞类别 C取消分裂
MODIFY_TYPE_LIST = ["A", "B", "C"]

"""质控任务参数配置"""
# 质控任务细胞最小数量
QC_WHITE_CELL_MIN_COUNT = 100
# 质控任务结果判定比例,大于该数为存在问题
QC_PERCENT_LIMIT = 0.05
# 质控任务结果选择对比图片时的数量
QC_SELECT_COUNT = 5
# 白细胞分割图半径尺寸
WHITE_CELL_SIZE = 165
# 红细胞分割图半径尺寸
RED_CELL_SIZE = int(15.4 * 11.5 * 0.5)
# 血小板浓度模块总行列
PC_TYPE_COLS = 4
# 根据go程序的common文件ReductionMultipleR、ReductionMultipleC中的数值改变的common文件ReductionMultipleR、ReductionMultipleC中的数值改变
ALL_RAW_IMAGE_PER_IMAGE_SIZE = 5
# 写入模块间隔多长时间写入一次
WRITE_INDEXS_INTERVAL = 5
# 写入模块最大缓存量写入一次
WRITE_INDEXS_FREQUENCY = 7500
# 允许导出的日志最大数量
EXPORT_LOGS_MAX_COUNT = 100000
# 允许导出的任务最大数量
EXPORT_TASKS_MAX_COUNT = 50000

"""PLT浓度计算参数"""
# 增加线
SEVERE_REDUCTION = 50
# 减少线
REDUCTION = 125
# 正常线
NORMAL = 350

# 瓦片地图与层级的换算关系
LEAFLET_LAYER = 4
# 地图最大层级数
MAP_LAST_LAYER_SERIES = 9
# 高倍视野系数
HIGH_VISUAL_FIELD_FACTOR = 0.379

"""图床路由"""
# 图片访问路由
PHOTO_URL = '/photo/%s/%s/%s'
# other文件夹图片访问路由
PHOTO_OTHER_URL = '/photo/%s/other/%s'
# 扫描进度图片访问路由
PHOTO_ALL_URL = '/photo/%s/other/%s/%s'
# 白细胞模块显微图片访问路由
PHOTO_RAW_URL = '/photo/%s/raw/%s'
# 质控模块显微图片访问路由
PHOTO_ORIGINAL_RAW_URL = '/photo/%s/original_raw/%s'
# 质控模块标准图片访问路由
STANDARD_IMAGE_URL = '/photo/%s/standard/%s'
# 白模块显微图片存储路径
PHOTO_RAW_IMAGE_PATH = "task_results/%s/raw/%s"
# 红模块显微图片存储路径
PHOTO_RED_RAW_IMAGE_PATH = "task_results/%s/red_raw/%s"
# 细胞分割图片存储路径
PHOTO_CELL_IMAGE_PATH = "task_results/%s/cell/%s"
# 白模块瓦片图片存储路径
PHOTO_TILE_PATH = "task_results/%s/tile"
# other图片存储路径
PHOTO_OTHER_IMAGE_PATH = "task_results/%s/other/%s"
# 疟疾模块瓦片图片存储路径
MAP_IMAGE_PATH = "task_results/%s/tile/%s/%s/%s"
# 红模块瓦片图片存储路径
MAP_RED_IMAGE_PATH = "task_results/%s/red_tile/%s/%s/%s"
# 白模块显微图片文件夹存储路径
RAW_IMAGES = 'task_results/%s/raw/'
# 血小板浓度计算模块显微图片文件夹存储路径
P_R_RAW_IMAGES = 'task_results/%s/platelet_raw/'
# 红模块显微图片文件夹存储路径
RED_RAW_IMAGES = 'task_results/%s/red_raw/'

"""分析结果路径"""
# 分析结果txt文件存储路径
CELL_LABEL_TXT_PATH = "task_results/%s/cell/%s/%s.txt"
# 分析结果txt文件夹存储路径
CELL_LABEL_FOLDER_PATH = "task_results/%s/cell/%s/%s"
# 分析结果细胞图片文件夹存储路径
CELL_LABEL_IMAGE_PATH = "task_results/%s/cell/%s/%s/%s"
# 分析结果模块类别文件夹存储路径
MODULE_FOLDER_PATH = "task_results/%s/cell/%s"
# 分析结果图片数据文件存储路径
CELL_LABEL_DAT_PATH = "task_results/%s/cell/%s/%s.dat"
# 显微图片数据文件存储路径
RAW_DAT_PATH = "task_results/%s/%s/%s.dat"
# 项目产生图片存储的文件夹路径
TASK_RESULT_PATH = os.path.join(IMAGE_ROOT, "task_results")

"""细胞中 英文类别文件存储路径"""
# 临床版细胞类别文件路径
RED_CLINICAL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/red_clinical_labels.txt")
PLATELET_CLINICAL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/platelet_clinical_labels.txt")
PC_CLINICAL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/platelet_concentration_labels.txt")
WHITE_CLINICAL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/white_clinical_labels.txt")
PC_LABEL_PATH = os.path.join(ROOT, "script/label_txt/platelet_concentration_labels.txt")
# 各个模型类别的全部细胞类别，包含科研版和临床版
RED_ALL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/red_all_labels.txt")
PLATELET_ALL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/platelet_all_labels.txt")
WHITE_ALL_LABEL_PATH = os.path.join(ROOT, "script/label_txt/white_all_labels.txt")
WHITE_XIEHE_LABEL_PATH = os.path.join(ROOT, "script/label_txt/white_xiehe_labels.txt")
# 科研版细胞类别文件路径
RED_SCIENTIFIC_LABEL_PATH = os.path.join(ROOT, "script/label_txt/red_scientific_labels.txt")
PLATELET_SCIENTIFIC_LABEL_PATH = os.path.join(ROOT, "script/label_txt/platelet_scientific_labels.txt")
WHITE_SCIENTIFIC_LABEL_PATH = os.path.join(ROOT, "script/label_txt/white_scientific_labels.txt")
# 疟疾
PARASITE_THICK_LABEL_PATH = os.path.join(ROOT, "script/label_txt/parasite_thick_labels.txt")
PARASITE_THIN_LABEL_PATH = os.path.join(ROOT, "script/label_txt/parasite_thin_labels.txt")

"""文件名称"""
# 配置文件名车给你
CONFIG_NAME = "cygnus.ini"
# python日志文件名称
CYGNUS_LOG_FILE_NAME = 'cygnus.log'
# 用户操作日志文件名称
CYGNUS_USER_LOG_FILE_NAME = 'user.log'
# 版本信息配置文件名称
PATENT_FILE_NAME = 'patent.ini'
# 血膜拟合图片名称
BLOOD_MODEL_NAME = "blood_model_image.png"
# 玻片缩略图片名称
SLIDE_THUMBNAIL_NAME = "slide_thumbnail.png"
# 玻片缩略瞬时旋转90度图片名称
SLIDE_VERTICAL_THUMBNAIL_NAME = "slide_vertical_thumbnail.png"
# 监控页面进度图片名称
IMAGE_ALL_MAP_NAME = "image_all_progress.jpg"
# 预扫描图片名称
PRE_IMAGE_NAME = "pre_image.jpg"
# 血小板浓度计算拼接图片名称
P_R_IMAGE_NAME = "PR.jpg"
# 白模块显微图片存储文件名称
RAW = "raw"
# 红模块显微图片存储文件名称
RED_RAW = "red_raw"
# 疟疾厚模块显微图片存储文件名称
THICK_RAW = "thick_raw"
# 疟疾薄模块显微图片存储文件名称
THIN_RAW = "thin_raw"
# 血小板浓度计算模块显微图片存储文件名称
PC_RAW = "pc_raw"
# 白模块瓦片地图存储文件名称
TILE = "tile"
# 疟疾薄模块瓦片地图存储文件名称
THIN_TILE = "thin_tile"
# 疟疾厚模块瓦片地图存储文件名称
THICK_TILE = "thick_tile"
# 红模块瓦片地图存储文件名称
RED_TILE = "red_tile"
# 血小板浓度计算模块瓦片地图存储文件名称
PC_TILE = "pc_tile"

# python日志筛选名称
PYTHON_TYPE = "python"
# 用户操作日志筛选名称
PRODUCT_TYPE = "product"
# go模块日志筛选名称
GO_TYPE = "Go"
# 下位机硬件模块日志筛选名称
HARDWARE_TYPE = "hardware"

"""扫描类型"""
# 按个数扫描
SCAN_COUNT = "Count"
# 按区域/体尾交接扫描
SCAN_AREA = "Area"
# 按全域扫描
SCAN_ALL = "All"

"""扫描模块名称"""
# 白模块
WHITE_TYPE = "White"
# 红模块
RED_TYPE = "Red"
# 血小板浓度计算模块
PC_TYPE = "PC"
# 血小板模块
PLATELET_TYPE = "Platelet"
# 寄生虫模块
PARASITE_TYPE = "Parasite"
# 寄生虫薄模块
PARASITE_THIN_TYPE = "Thin"
# 寄生虫厚模块
PARASITE_THICK_TYPE = "Thick"
# 寄生虫厚薄模块
PARASITE_THICK_THIN_TYPE = "ThickThin"
# 寄生虫模块列表
PARASITE_SCAN_TYPE_LIST = [PARASITE_THIN_TYPE, PARASITE_THICK_TYPE, PARASITE_THICK_THIN_TYPE]
# 质控模块
QC_TYPE = "QC"
QC_TYPE_LOWER = "qc"
# 该项目允许创建的模块类别列表
MODULE_TYP_LIST = ["White", "Red", "Platelet", "Parasite"] + PARASITE_SCAN_TYPE_LIST

"""进程名称"""
GO_PROCESS_NAME = "main-go"
# 算法进程
ENGINEER_ALGO_PROCESS_NAMES = ['RSF1', 'RSF2', 'PSF', 'ST', "DracoPlusPlus", "RSO"]
# go模块进程
SOCKET_PROCESS_NAME = ['socket_flask']
# 项目启动之后应应存活的进程名称
PROCESS_NAMES = ENGINEER_ALGO_PROCESS_NAMES + [GO_PROCESS_NAME]
