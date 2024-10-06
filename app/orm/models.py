"""
该模块用于建立数据库映射，数据库中字段在这修改进行
"""

import datetime
import json

from pypinyin import lazy_pinyin

# 1.
# Label表：用于存储系统细胞类别信息
# 2.
# User表：用于存储系统用户注册信息
# 3.
# Role表：用于存储系统用户权限信息
# 4.
# Patient表：用于存储病人信息
# 5.
# Task表：用于存储任务创建信息和任务析结果
# 6.
# TaskSort任务排序表：用于存储任务排序结果
# 7.
# TaskSubsidiary任务子表：用于存储任务收藏图片和不合格图片结果
# 8.
# Platelet血小板表：用于存储血小板任务结果
# 9.
# PC表：用于存储质控任务结果
# 10.
# Red表：用于存储红模块任务结果
# 11.
# White表：用于存储白模块任务结果
# 12.
# Parasite表：用于存储疟疾模块信息
# 13.
# Parameter表：用于存储软件唯一编号和一些可修改的参数
# 14.
# Log表：用于存储用户可用于审计的操作信息
# 15.
# Report表：用于存储报告信息
# 16.
# Box表：用于存储玻片盒使用次数计算表信息
# 17.
# Size表：用于存储临床版本红模块大、小尺寸表信息
# 18.
# Code表：用于存储油袋信息
# 19.
# ImageQuality表：用于存标识图片是否舒展数据库信息
# 20.
# SetUp表：用于存标识系统设置参数数据库信息

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float, func, text,JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RedLabel(Base):
    """红细胞类别信息表"""
    __tablename__ = 'red_label'
    id = Column(Integer, primary_key=True, index=True)
    # 细胞英文名字
    en = Column(String)
    # 细胞中文名字
    ch = Column(String)
    # 大类别：正常、异常、其它、自定义等：Normal,Abnormal,Other,SelfDefine
    large_categories = Column(String)


class WhiteLabel(Base):
    """白细胞类别信息表"""
    __tablename__ = 'white_label'
    id = Column(Integer, primary_key=True, index=True)
    # 细胞英文名字
    en = Column(String)
    # 细胞中文名字
    ch = Column(String)
    # 大类别：正常、异常、其它、自定义等：Normal,Abnormal,Other,SelfDefine
    large_categories = Column(String)


class PlateletLabel(Base):
    """血小板细胞类别信息表"""
    __tablename__ = 'platelet_label'
    id = Column(Integer, primary_key=True, index=True)
    # 细胞英文名字
    en = Column(String)
    # 细胞中文名字
    ch = Column(String)
    # 大类别：正常、异常、其它、自定义等：Normal,Abnormal,Other,SelfDefine
    large_categories = Column(String)


class ThinLabel(Base):
    """疟疾薄类别信息表"""
    __tablename__ = 'thin_label'
    id = Column(Integer, primary_key=True, index=True)
    # 细胞英文名字
    en = Column(String)
    # 细胞中文名字
    ch = Column(String)
    # 大类别：正常、异常、其它、自定义等：Normal,Abnormal,Other,SelfDefine
    large_categories = Column(String)


class ThickLabel(Base):
    """疟疾厚类别信息表"""
    __tablename__ = 'thick_label'
    id = Column(Integer, primary_key=True, index=True)
    # 细胞英文名字
    en = Column(String)
    # 细胞中文名字
    ch = Column(String)
    # 大类别：正常、异常、其它、自定义等：Normal,Abnormal,Other,SelfDefine
    large_categories = Column(String)


class MicroLabel(Base):
    """微生物类别信息表"""
    __tablename__ = 'micro_label'
    id = Column(Integer, primary_key=True, index=True)
    # 细胞英文名字
    en = Column(String)
    # 细胞中文名字
    ch = Column(String)
    # 大类别：正常、异常、其它、自定义等：Normal,Abnormal,Other,SelfDefine
    large_categories = Column(String)


class User(Base):
    """用户表"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    # 用户名
    user_name = Column(String, nullable=False)
    # 用户密码
    password_hash = Column(String, nullable=False)
    # 用户角色:分为operator操作员1、auditor审核员2、admin管理员3、maintenance工程师账户0
    # 用户角色
    role = Column(Integer, nullable=False)
    # 用户创建时间
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 用户信息更新时间
    update_time = Column(DateTime)
    # 预留字段，用于保存用户名
    is_saved = Column(Boolean, default=False)
    # 用户是否删除
    deleted = Column(Boolean, default=False)


class Role(Base):
    """权限表"""
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    # 权限级别标识符
    role_id = Column(String, nullable=False)
    # 权限中文名称
    role_name = Column(String, nullable=False)
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now)


class UserRole(Base):
    """用户表"""
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # 用户名
    hashed_password = Column(String, nullable=False)  # 加密后的密码
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)  # 关联角色
    role = relationship("Role")  # 定义与 Role 的关系


class Patient(Base):
    """病人信息表"""
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    # 患者姓名
    patient_name = Column(String)
    # 患者ID
    patient_id = Column(String)
    # 患者性别
    gender = Column(Integer)
    # 患者年龄
    age = Column(String)
    # 科室名称
    department = Column(String)
    # 床号
    bed_id = Column(String)
    # 费用类别
    pay_type = Column(String)
    # 标本类型
    sample_type = Column(String)
    # 送检医师ID
    submission_doc_id = Column(String)
    # 送检医师姓名
    submission_doc_name = Column(String)
    # 申请单号
    application_id = Column(String)
    # 送检时间
    application_time = Column(DateTime, default=datetime.datetime.now)
    # 检验医师ID
    inspect_doc_id = Column(String)
    # 检验医师姓名
    inspect_doc_name = Column(String)
    # 核对医师ID
    verify_doc_id = Column(String)
    # 核对医师姓名
    verify_doc_name = Column(String)

    patient_name_pinyin = Column(String)
    submission_doc_name_pinyin = Column(String)

    def __init__(self, patient_name, submission_doc_name):
        self.patient_name = patient_name
        self.submission_doc_name = submission_doc_name
        self.update_patient_name_pinyin()
        self.update_submission_doc_name_pinyin()

    def update_patient_name_pinyin(self):
        self.patient_name_pinyin = ''.join([word[0].lower() for word in lazy_pinyin(self.patient_name)])

    def update_submission_doc_name_pinyin(self):
        self.submission_doc_name_pinyin = ''.join([word[0].lower() for word in lazy_pinyin(self.submission_doc_name)])


class Task(Base):
    """任务表"""
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    # 创建该任务的操作员
    create_user = Column(String)
    # 玻片号
    slide_id = Column(String)
    # 患者id
    patient_id = Column(Integer)
    # 任务创建时间
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 任务结束时间
    finish_time = Column(DateTime)
    # 任务状态
    status = Column(String)
    # Blood / Malaria
    task_type = Column(String)
    # 是否审核，审核者
    auditor = Column(String)
    # 任务是否收藏
    is_favorite = Column(Boolean, default=False)
    # 身份证号码
    ID = Column(String)
    # 存储区域划分，体尾交界处，只有白细胞有
    rows_cols = Column(Text)
    # 该任务所有的细胞名称
    label_list = Column(Text)
    # 全玻片任务，最近一次查看细胞的范围
    last_viewed_area = Column(Text)
    # 文件夹路径，会被备份模块修改
    scan_file_path = Column(String)
    # 扫描模式：（白、红、寄生虫、血小板）
    scan_mode = Column(Text)
    # 进度信息
    progress = Column(Float)
    # 标记删除
    deleted = Column(Boolean, default=False)
    # 再次进入任务时，是否提示不合格图片
    is_hint = Column(Boolean, default=True)
    # 槽位位置
    slot = Column(Integer)
    # 玻片盒编码
    box_no = Column(String(64))
    # 扫描方式
    scan_type = Column(String)
    # 是否可退出玻片
    is_out = Column(Boolean, default=True)
    # 玻片是否平整
    flatness = Column(Boolean, default=True)
    # 失败原因
    failure_reason = Column(String)
    # # 疟疾模块任务分析结果
    # parasite_id = Column(Integer, ForeignKey('parasite.id'), nullable=False)
    # # 白模块任务分析结果
    # white_id = Column(Integer, ForeignKey('white.id'), nullable=False)
    # # 红模块任务分析结果
    # red_id = Column(Integer, ForeignKey('red.id'), nullable=False)
    # # 血小板模块任务分析结果
    # platelet_id = Column(Integer, ForeignKey('platelet.id'), nullable=False)
    # 任务子表
    task_subsidiary_id = Column(Integer, ForeignKey('task_subsidiary.id'), nullable=False)
    # 红模块任务分析结果
    qc_id = Column(Integer, ForeignKey('qc.id'), nullable=False)
    # 是否删除图片
    is_deleted_image = Column(Boolean, default=False)
    # 备注
    notes = Column(String)
    # 标识该任务是否不舒展分析
    not_stretching = Column(Boolean)
    # 取消正在扫描任务后，是否保留当前数据
    is_save_data = Column(Boolean, default=False)


class TaskSort(Base):
    """任务排序表"""
    __tablename__ = 'task_sort'
    id = Column(Integer, primary_key=True, index=True)
    # 任务id
    task_id = Column(Integer, nullable=False)
    # 任务创建时间
    # create_time = Column(DateTime, default=datetime.datetime.now)
    status = Column(String)
    # 任务加急时间
    urgent_time = Column(DateTime)
    # 任务置顶时间
    up_time = Column(DateTime)
    # 创建急诊位时间
    emergency_time = Column(DateTime)
    # 槽位位置
    slot = Column(Integer)


class TaskSubsidiary(Base):
    """任务子表"""
    __tablename__ = 'task_subsidiary'
    id = Column(Integer, primary_key=True, index=True)
    # 不合格图片
    disqualification = Column(Text)
    # 收藏的图片
    pic_list = Column(Text)


class Platelet(Base):
    """血小板表"""
    __tablename__ = 'platelet'
    id = Column(Integer, primary_key=True, index=True)
    # 血小板模块任务分析结果
    platelet_result = Column(Text)
    # 血小板统计信息
    platelet_statistics = Column(Text)


class QC(Base):
    """质控表"""
    __tablename__ = 'qc'
    id = Column(Integer, primary_key=True, index=True)
    # 质控任务结论
    qc_conclusion = Column(String)
    # 质控任务结果
    qc_result = Column(Text)


class Red(Base):
    """红模块表"""
    __tablename__ = 'red'
    id = Column(Integer, primary_key=True, index=True)
    # 红细胞模块任务分析结果
    red_result = Column(Text)
    # 红细胞阈值数据
    red_ration_result = Column(Text)
    # 红细胞默认阈值
    red_threshold = Column(Text)


class White(Base):
    """白模块表"""
    __tablename__ = 'white'
    id = Column(Integer, primary_key=True, index=True)
    # 白细胞模块任务分析结果 {"label_count":{"AR": 9,}, "collection": [1-2,2-1]}
    white_result = Column(Text)
    # 有核红信息
    nuclear_red = Column(Text)


class Parasite(Base):
    """疟疾表"""
    __tablename__ = 'parasite'
    id = Column(Integer, primary_key=True, index=True)
    # 任务ID
    task_id = Column(Integer, index=True)
    # 任务信息
    # task_info = relationship('Task', backref='parasite')
    # 疟疾薄
    parasite_thin_result = Column(Text)
    # 疟疾厚
    parasite_thick_result = Column(Text)
    # 恶性疟原虫
    falciparum_count = Column(Integer, default=0)
    # 间日疟原虫
    vivax_count = Column(Integer, default=0)
    # 三日疟原虫
    malariae_count = Column(Integer, default=0)
    # 卵形疟原虫
    oval_count = Column(Integer, default=0)
    # 环状体
    annuli_count = Column(Integer, default=0)
    # 大滋养体
    trophozoites_count = Column(Integer, default=0)
    # 繁殖体
    schizont_count = Column(Integer, default=0)
    # 配子体
    gametophyte_count = Column(Integer, default=0)
    # 感染率
    infection_rate = Column(Integer, default=0)
    # 密度
    density = Column(Integer, default=0)
    # 扫描结果,阴性或阳性
    parasite_conclusion = Column(Boolean, default=False)
    # 白细胞数量
    white_count = Column(Integer, default=0)
    # 红细胞数量
    red_count = Column(Integer, default=0)


class Micro(Base):
    """微生物模块表"""
    __tablename__ = 'micro'
    id = Column(Integer, primary_key=True, index=True)
    # 任务ID
    task_id = Column(Integer, index=True)
    # 微生物模块任务分析结果
    micro_result = Column(Text)


class Parameter(Base):
    """参数表"""
    __tablename__ = 'parameter'
    id = Column(Integer, primary_key=True)
    parameter = Column(String)
    # 软件当前扫描顺序，包括一个任务是否加急是否置顶等信息
    scan_sequence = Column(Text)
    # 扫描模式
    scan_mode = Column(Text)

    # TODO 标识科研版与临床版
    is_scientific = Column(Boolean, default=False)


class Log(Base):
    """操作日志表"""
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    # 操作动作
    target = Column(String)
    # 操作人员
    operator = Column(String)
    # TODO 操作级别
    operation_type = Column(String)
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now)


class Report(Base):
    """病人报告表"""
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    # 任务ID
    task_id = Column(Integer, nullable=False)
    # 用户ID
    user_id = Column(Integer, nullable=False)
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 新的报告内容
    content = Column(Text)
    # 原始报告内容
    raw_content = Column(Text)
    # 报告是否修改
    is_modified = Column(Boolean, default=False)


class Box(Base):
    """玻片盒使用次数计算表"""
    __tablename__ = 'box'
    id = Column(Integer, primary_key=True)
    # 玻片盒编码
    code = Column(String, nullable=False)
    # 玻片盒编码已使用数量
    code_count = Column(Integer, nullable=False)


class Size(Base):
    """临床版本红模块大、小尺寸表"""
    __tablename__ = 'size'
    id = Column(Integer, primary_key=True)
    # 默认红细胞阈值
    threshold = Column(Text, default=json.dumps({}))
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now)


class Code(Base):
    """油袋表"""
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    # code码
    code_ = Column(String)
    # 是否使用
    is_used = Column(Boolean, default=False)
    # 更新时间
    update_time = Column(DateTime, default=datetime.datetime.now)


class ImageQuality(Base):
    """标识图片是否舒展数据库表"""
    __tablename__ = 'image_quality'
    id = Column(Integer, primary_key=True, index=True)
    # 任务ID
    task_id = Column(Integer)
    # 图片数据
    image_data = Column(Text)


# class SetUp(Base):
#     """系统设置参数数据库表"""
#     __tablename__ = 'set_up'
#     id = Column(Integer, primary_key=True, index=True)
#     # 扫描模式
#     scan_mode = Column(Text, default=json.dumps(scan_mode))
#     # 扫描模式触发规则定义
#     rules = Column(String, default=json.dumps(rules))
#     # 扫描模块
#     scan_module = Column(Text, default=json.dumps(scan_module))
#     # 报告设置
#     report_set = Column(Text, default=json.dumps(report_set))
#     # 字体大小
#     font_size = Column(String)
#     # 细胞类别顺序
#     label_order = Column(Text, default=json.dumps(LabelEnChBase.get_instance().label_order_dic()))


class EngineerExport(Base):
    """是否打开导出选项配置表"""
    __tablename__ = 'engineer_export'
    id = Column(Integer, primary_key=True, index=True)
    # 是否可导出文件
    mark_file = Column(Boolean, default=False)
    # 是否可导出数据
    mark_data = Column(Boolean, default=False)


class EngineerImage(Base):
    """图片相关配置表"""
    __tablename__ = 'engineer_image'
    id = Column(Integer, primary_key=True, index=True)
    # 图片宽
    image_width = Column(Boolean, default=False)
    # 图片高
    image_height = Column(Boolean, default=False)
    # 扫描大图宽等于多少微米
    image_width_px_um = Column(Boolean, default=False)


class EngineerHardware(Base):
    """硬件相关配置表"""
    __tablename__ = 'engineer_hardware'
    id = Column(Integer, primary_key=True, index=True)


class EngineerSoftware(Base):
    """硬件相关配置表"""
    __tablename__ = 'engineer_software'
    id = Column(Integer, primary_key=True, index=True)
    # 不舒展阈值
    stretching_count = Column(Integer, default=8)
    # 扫描大图1微米等于多少像素
    um_px = Column(Integer, default=9)


class Mark(Base):
    """"系统标注表"""
    __tablename__ = 'mark'
    id = Column(Integer, primary_key=True, index=True)
    #
    mark_file = Column(Boolean, default=False)

    mark_data = Column(Boolean, default=False)


class I18N(Base):
    """翻译"""
    __tablename__ = 'i18n'
    id = Column(Integer, primary_key=True, index=True)
    language_code = Column(String, default="zh")
    create_time = Column(DateTime, default=datetime.datetime.now)
    select_languages = Column(Text,
                              default=json.dumps({"zh": "中文", "en": "英文"}))


class VersionConfiguration(Base):
    """版本相关配置表"""
    __tablename__ = 'version_configuration'
    id = Column(Integer, primary_key=True, index=True)
    project_version = Column(String, default="Blood_1")
    select_versions = Column(Text, default=json.dumps({
        "Blood_1 ": "外周血-I30",
        "Blood_2  ": "外周血-T5",
        "Malaria_1": "疟疾-I30",
        "Malaria_2": "疟疾-T5",
        "Micro_1": "微生物-I30",
        "Micro_2": "微生物-T5",
    }))
    create_time = Column(DateTime, default=datetime.datetime.now)


class VersionInfo(Base):
    """版本信息"""
    __tablename__ = 'version_info'
    id = Column(Integer, primary_key=True, index=True)
    version_name = Column(String, unique=True, index=True, server_default=text("'Blood_2'"))
    software_python = Column(String, server_default=text("'Python 3.9'"))
    software_ui = Column(String, server_default=text("'UI v1.1'"))
    software_go = Column(String, server_default=text("'Go 1.16'"))
    hardware = Column(String, server_default=text("'Hardware v1.1'"))
    alg_white = Column(String, server_default=text("'Alg_w v1.1'"))
    alg_red = Column(String, server_default=text("'Alg_r v1.1'"))
    alg_pc = Column(String, server_default=text("'Alg_p v1.1'"))
    release_num = Column(String, server_default=text("'1.1'"))
    # 创建时间
    create_time = Column(DateTime, server_default=func.now())


class StretchingThreshold(Base):
    """不舒展阈值"""
    __tablename__ = 'stretching_threshold'
    id = Column(Integer, primary_key=True, index=True)
    stretching_size = Column(Float, server_default=text("'1.1'"))


class AlgorithmThreshold(Base):
    """算法阈值存储"""
    __tablename__ = 'algorithm_threshold'
    id = Column(Integer, primary_key=True, index=True)
    white_size = Column(Float, server_default=text("73"))
    red_size = Column(Float, server_default=text("73"))
    pc_size = Column(Float, server_default=text("165"))
    thick_size = Column(Float, server_default=text("165"))
    platelet_size = Column(Float, server_default=text("165"))
    micro_size = Column(Float, server_default=text("165"))


class Test(Base):
    """版本相关配置表"""
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True, index=True)
    # 不舒展阈值
    version_ = Column(Text, default=json.dumps({"Blood": "外周血", "Malaria": "疟疾"}))




class SimulationData(Base):
    """数据模拟"""
    __tablename__ = 'simulation_data'
    id = Column(Integer, primary_key=True, index=True)
    # 列出日志文件模拟
    log_modules = Column(JSON)
    # 数据备份模拟
    data_backup = Column(JSON)
    # 数据搜索模拟
    data_search = Column(JSON)
    # Python Go 服务器状态模拟
    go_server = Column(JSON)
    # 硬件状态信息模拟
    hardware_status = Column(JSON)
    # 更新标记数据
    set_mark_hide = Column(JSON)
    # 动态路由模拟
    async_router = Column(JSON)
    # get hide 模拟
    get_hide = Column(JSON)
    # config 模拟
    config = Column(JSON)
    # 软硬件重启模拟
    restart = Column(JSON)




