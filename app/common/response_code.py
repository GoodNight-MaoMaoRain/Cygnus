# coding:utf-8

# 错误码
class RET:
    OK = "0"
    IdleMode = "1003"
    SelfDiagnose = "1004"
    SentOK = "1005"
    SlideStartscan = "1006"
    SlideFinishscan = "1007"
    FavoriteOK = "1008"
    UsedNormal = "1009"
    Normal = "1010"
    PasswdLessThan6digits = "2001"
    UsernameLessThan5digits= "2002"
    USERNAMEORPWDERR = "2003"
    NewPasswdtTwicIsInconsistent = "2004"
    PleaseCorrectUsernameOrPasswd = "2005"
    USERNAMEERR = "2006"
    USERERR = "2007"
    BUSY = "2008"
    SystemAutoDeletAndNotCreateTask = "2009"
    RunTasksModifiedTaskList = "2010"
    ModifiedTaskAlreadyQCTask = "2011"
    BatchCancelTaskRunTask = "2012"
    TaskRunAndExportTaskIsCompleted = "2013"
    NotFinishTaskQC = "2014"
    TaskQCNormal = "2015"
    TaskNormal = "2016"
    TaskQC = "2017"
    CountInsufficient = "2021"
    SameSample = "2023"
    ManualShutdownFomSoftware= "2024"
    AutoShutdownFomSoftware = "2025"
    ManualShutdownFomHardware = "2026"
    AutoShutdownFomHardware = "2027"
    NoSlideBox = "2028"
    AuditorUpperLimit = "2029"
    OperatorUpperLimit = "2030"
    PermissionMaximumLimitTen = "2031"
    PermissionMaximumLimitOne = "2032"
    StartScanMany = "2033"
    OilTen = "2034"
    OilFive = "2035"
    CacheFull = "2036"
    CameraNotConnected = "2037"
    SlideBoxEmpty = "2038"
    UserCancelPleaseRescan = "2039"
    SpaceInsufficienCleanTimely = "2040"
    AutomaticDeletionCannotScanTask = "2041"
    ReplaceSlideBox = "2042"
    QRCodeFailed = "2043"
    SelfDiagnoseUnableCreateTask = "2044"
    LengthNoteNot400Char= "2045"
    LengthPatientNameIDNot40Char = "2046"
    LengthSlideIDNot20Char = "2047"
    LengthInspectionNot20Char = "2048"
    LengthPatientNameIDSlideNot40Char = "2049"
    FavouriteCellReached40 = "2050"
    PreviousStepsNotCompleted = "2051"

    UNKOWNERR = "3001"
    NODATA = "3002"
    NetworkError = "3003"
    QueryFailed = "3004"
    DataUpdateFailed = "3005"
    MISSPAR = "3006"
    PARAMERR = "3008"
    PARAMFormatERR = "3009"
    PARAMVerifiedERR = "3010"
    PasswdModifydFailed = "3011"
    EnterCorrectAccountPasswd = "3012"
    UserLoginERR = "3013"
    SESSIONERR = "3014"
    LoginERR = "3015"
    LogoutERR = "3016"
    ClearLoginERR = "3017"
    MISSTOKEN = "3018"
    NOPRIVILEGE = "3019"
    PrivilegeVerifiedFailed = "3020"
    AddUserFailed = "3021"
    DeleteUserFailed = "3022"
    QueryUserFailed = "3023"
    ControlSoftwareFailure = "3024"
    CountErr = "3025"
    SlideBoxLoadErr = "3026"
    SlideGetFailed = "3027"
    SentFailed = "3028"
    ExportFailed = "3029"
    RetrievalFailed = "3030"
    ResetFailed = "3031"
    AuditFailed = "3032"
    CancelAuditFailed = "3033"
    UpFailedNoScanTaskRun = "3034"
    TopTaskFailed = "3035"
    TaskFailure = "3036"
    TaskInfoQueryFailure = "3037"
    TaskQueryFailure = "3038"
    TaskNotFound = "3039"
    RestartBackendFailed = "3040"
    ModifyScanModeFailed = "3041"
    GetbloodFailed = "3042"
    SplitFailed = "3043"
    AddCellFailed = "3044"
    FavoriteCellFailed = "3045"
    FavoriteTaskFailed = "3046"
    DeleteTaskFailed = "3047"
    SwitchTaskFailed = "3048"
    CellLocalizationFailure = "3049"
    TaskListQueryFailed = "3050"
    TaskInfoGetFailure = "3051"
    CurrentTaskQueryFailed = "3052"
    PageTaskQueryFailed = "3053"
    StatisticalERR = "3054"
    TaskNotData = "3055"
    TaskNotExist = "3056"
    GetRowAndColInfoFailed = "3057"
    GetImageInfoFailed = "3058"
    OrganizaInfoERR = "3059"
    TaskCellInfoQueryFailed = "3060"
    TaskCellInfoFailed = "3061"
    GetImageNotExist= "3062"
    GetCategoryDataFailed = "3063"
    NotQueryInfoFound = "3064"
    ScanStartupFailed = "3065"
    RequestScanFailed = "3066"
    CancelScanTaskToHardwareSendFailed = "3067"
    OrganizaSearchInfoFailed = "3068"
    ReadCopyrightInfoFailed = "3069"
    RemarkRecordFailed = "3070"
    ImageQualityJudgmentERR = "3071"
    DBCOMMITERR = "3072"
    DBQUERYERR = "3073"
    DBUPDATEERR = "3074"
    ImageProcessModuleNotStarted = "3075"
    ImageAnalysisModuleStartFailed = "3076"
    FileIOERR = "3077"
    FileNotExist = "3078"
    FileReadFailed = "3079"
    FileLocaWriteFailed = "3080"
    FileCompressERR = "3081"
    FileExportErr = "3082"
    DataTooLargePleaseReselectSearchExport = "3083"
    DataTooLargePleaseReseleDateExport = "3084"
    CellNumberInsufficient = "3085"
    QCTaskCellNumberInsufficient = "3086"
    QCTaskInfoQueryFailed = "3087"
    StandardImageInfoQueryFailed = "3088"
    QCImageNotExist = "3089"
    StandardImageNotExist = "3090"
    QCTaskInfoUpdateFailed = "3091"
    SoftwareSidePleasePauseUseAndContactEngineer = "3092"
    DetectedZeroCellsUnableEvaluate = "3093"
    PleaseCheckHardware = "3094"
    AbnormalClarityQCFailed = "3095"
    TemperatureHigh = "3096"
    OilLowNoScan = "3097"
    NoHardware = "3098"
    SlideNotRecognizedTaskCreatFailed = "3099"
    ScanErr = "3100"
    CreateScanTaskFailed = "3101"
    CreateTaskFailed = "3102"
    WhiteCellClassCountFailed = "3103"
    PlateletAnalysisFailed = "3104"
    PlateletCountAnalysisFailed = "3105"
    RedCellAnalysisFailed = "3106"
    QueryParameterTableFailed = "3107"
    QueryCriteriaSpecialChar = "3108"
    QueryPatientNameERR = "3109"
    QueryPatientInfoERR = "3110"
    QueryCurrentSystemVersionFailed = "3111"
    QuerySystemInfoFailed = "3112"
    SystemInfoSaveFailed = "3113"
    QueryRuleSettingInfoFailed = "3114"
    RuleSettingInfoSaveFailed = "3115"
    RecordUserLoginInfoFailed = "3116"
    ChangeUserLoginInfoFailed = "3117"
    QCReportNotViewedOrModify = "3118"
    GetReportFailed = "3119"
    ModifReportFailed = "3120"
    ReportInfoQueryFailed = "3121"
    PrintingException = "3122"

    GetCurrentLanguageFailed = '3141'
    CreateDefaultLanguageFailed = '3142'
    GetCurrentVersionFailed = '3143'
    ParseSelectLanguagesFailed = '3144'
    GetLanguageInfoFailed = '3145'
    GetLanguageRecordFailed = '3146'
    LanguageNotAllowed = '3147'
    UpdateLanguageFailed = '3148'
    SetLanguageFailed = '3149'
    GetThresholdsDataFailed = '3150'
    NoThresholdsFound = '3151'
    GetThresholdsInfoFailed = '3152'
    AddThresholdsFailed = '3153'
    UpdateThresholdsFailed = '3154'
    SetThresholdsFailed = '3155'
    GetVersionConfigFailed = '3156'
    CreateVersionConfigFailed = '3157'
    VersionNotFound = '3158'
    UpdateVersionInfoFailed = '3159'
    SetCurrentVersionFailed = '3160'
    GetVersionInfoFailed = '3161'
    CurrentVersionNotSet = '3162'
    SetVersionInfoFailed = '3163'
    DBUpdateError = '3164'
    DBQueryError = '3165'
    TaskExportError = '3166'
    TaskAddError = '3167'
    TaskDBExportError = '3168'
    TaskDBOperationError = '3169'
    TaskExportFailure = '3170'
    GetUaxisCodeFailed = '3171'
    GetSysCodeFailed = '3172'
    GetHardwareStatusFailed = '3173'
    ProcessHardwareStatusDataFailed = '3174'

    GetPythonLogFilesFailed = '3175'
    GetProductLogFilesFailed = '3176'
    GetGoLogFilesFailed = '3177'
    GetPythonLogFileListFailed = '3178'
    GetProductLogFileListFailed = '3179'
    GetGoLogFileListFailed = '3180'
    ReadLogFileFailed = '3181'
    FileCompressFailed = '3182'
    LogModuleTypeError = '3183'
    FileDownloadFailed = '3184'
    LogFilterFailed = '3185'
    TimeFormatError = '3186'
    SaveHardwareLogFailed = '3187'
    InvalidModuleTypeError = '3188'
    LogPaginationError = '3189'
    LogFilePathError = '3190'
    QueryLogInfoFailed = '3191'

    SysStatusQueryFailed = '3192'
    SensorStatusQueryFailed = '3193'
    TopCommandQueryFailed = '3194'
    NvidiaCommandQueryFailed = '3195'
    PythonServerQueryFailed = '3196'
    GoServerQueryFailed = '3197'
    DiskInfoQueryFailed = '3198'
    MemoryInfoQueryFailed = '3199'
    InternalStorageQueryFailed = '3200'
    CpuInfoQueryFailed = '3201'
    GpuInfoQueryFailed = '3202'
    SystemStatusQueryFailed = '3203'


# 错误码及描述
RET_TRANSLATE = {
    RET.OK: u"成功",
    RET.IdleMode: u"待机状态",
    RET.SelfDiagnose: u"自检状态中",
    RET.SentOK: u"发送成功",
    RET.SlideStartscan: u"玻片[]开始扫描",
    RET.SlideFinishscan: u"玻片[]扫描完成",
    RET.FavoriteOK: u"收藏成功",
    RET.UsedNormal: u"可以正常使用",
    RET.Normal: u"正常",
    RET.PasswdLessThan6digits: u"密码少于6位数",
    RET.UsernameLessThan5digits: u"用户名长度少于5位数",
    RET.USERNAMEORPWDERR: u"用户名或密码错误",
    RET.NewPasswdtTwicIsInconsistent: u"新密码两次输入不一致",
    RET.PleaseCorrectUsernameOrPasswd: u"请输入正确的账号密码",
    RET.USERNAMEERR: u"用户名不存在",
    RET.USERERR: u"用户不存在",
    RET.BUSY: u"有任务正在运行",
    RET.SystemAutoDeletAndNotCreateTask: u"系统正在执行自动删除程序，不可创建扫描任务",
    RET.RunTasksModifiedTaskList: u"修改的任务列表中有正在运行的任务",
    RET.ModifiedTaskAlreadyQCTask: u"修改的任务已有质控任务",
    RET.BatchCancelTaskRunTask: u"批量取消的任务中含有正在运行的任务",
    RET.TaskRunAndExportTaskIsCompleted: u"有任务在运行,任务运行结束后再进行导出",
    RET.NotFinishTaskQC: u"有未完成的质控任务",
    RET.TaskQCNormal: u"质控和普通任务同时在运行。",
    RET.TaskNormal: u"普通任务在运行。",
    RET.TaskQC: u"质控任务在运行。",
    RET.CountInsufficient: u"细胞数量不足",
    RET.SameSample: u"样本号已使用",
    RET.ManualShutdownFomSoftware: u"软件端人工终止",
    RET.AutoShutdownFomSoftware: u"软件端自动终止",
    RET.ManualShutdownFomHardware: u"扫描仪端人工终止",
    RET.AutoShutdownFomHardware: u"扫描仪端自动终止",
    RET.NoSlideBox: u"当前未放入玻片盒",
    RET.AuditorUpperLimit: u"审核员用户数量达到上限",
    RET.OperatorUpperLimit: u"操作员用户数量达到上限",
    RET.PermissionMaximumLimitTen: u"该权限用户数量已达上限10个",
    RET.PermissionMaximumLimitOne: u"该权限用户数量已达上限1个",
    RET.StartScanMany: u"请勿重复启动。",
    RET.OilTen: u"油量剩余10%",
    RET.OilFive: u"油量剩余5%",
    RET.CacheFull: u"缓存区域已满",
    RET.CameraNotConnected: u"相机未连接",
    RET.SlideBoxEmpty: u"玻片盒为空",
    RET.UserCancelPleaseRescan: u"用户取消 ，如需要请重新扫描",
    RET.SpaceInsufficienCleanTimely: u"检测到系统存储空间剩余不足，无法创建扫描任务，请及时清理",
    RET.AutomaticDeletionCannotScanTask: u"系统正在执行自动删除程序，不可创建扫描任务",
    RET.ReplaceSlideBox: u"检测到推片盒使用次数过多，可能影响玻片扫描质量，建议更换新的推片盒",
    RET.QRCodeFailed: u"推片盒信息识别获取失败，请检查推片盒二维码或更换新的推片盒",
    RET.SelfDiagnoseUnableCreateTask: u"自检过程中，无法创建扫描任务",
    RET.LengthNoteNot400Char: u"备注长度不允许超过400字符！",
    RET.LengthPatientNameIDNot40Char: u"患者姓名或ID长度不允许超过40！",
    RET.LengthSlideIDNot20Char: u"玻片号长度不允许超过20！",
    RET.LengthInspectionNot20Char: u"送检医师名称长度不允许超过40！",
    RET.LengthPatientNameIDSlideNot40Char: u"患者姓名ID/玻片号长度不允许超过40！",
    RET.FavouriteCellReached40: u"收藏细胞个数已达到40个！",
    RET.PreviousStepsNotCompleted: u"前面步骤尚未完成",

    RET.UNKOWNERR: u"未知错误",
    RET.NODATA: u"无数据",
    RET.NetworkError: u"网络故障",
    RET.QueryFailed: u"查询失败",
    RET.DataUpdateFailed: u"数据更新失败",
    RET.MISSPAR: u"参数不完整",
    RET.PARAMERR: u"参数错误",
    RET.PARAMFormatERR: u"参数格式错误",
    RET.PARAMVerifiedERR: u"参数校验出错！",
    RET.PasswdModifydFailed: u"密码修改失败，请重试",
    RET.EnterCorrectAccountPasswd: u"请输入正确的账号密码",
    RET.UserLoginERR: u"用户登录失败",
    RET.SESSIONERR: u"用户未登录",
    RET.LoginERR: u"登录失败，请重试",
    RET.LogoutERR: u"退出登录失败",
    RET.ClearLoginERR: u"清空登录状态失败",
    RET.MISSTOKEN: u"token缺失",
    RET.NOPRIVILEGE: u"权限不足",
    RET.PrivilegeVerifiedFailed: u"权限校验失败",
    RET.AddUserFailed: u"添加用户失败",
    RET.DeleteUserFailed: u"删除用户失败",
    RET.QueryUserFailed: u"用户信息查询失败",
    RET.ControlSoftwareFailure: u"控制软件故障",
    RET.CountErr: u"数量错误",
    RET.SlideBoxLoadErr: u"玻片盒装载错误，请联系技术人员检查设备。",
    RET.SlideGetFailed: u"玻片号读取失败，请手动录入信息",
    RET.SentFailed: u"发送失败",
    RET.ExportFailed: u"导出失败",
    RET.RetrievalFailed: u"检索失败，请重试",
    RET.ResetFailed: u"重置失败",
    RET.AuditFailed: u"审核失败",
    RET.CancelAuditFailed: u"取消审核失败",
    RET.UpFailedNoScanTaskRun: u"置顶失败-无扫描任务运行",
    RET.TopTaskFailed: u"置顶任务失败",
    RET.TaskFailure: u"任务失败",
    RET.TaskInfoQueryFailure: u"任务信息查询失败",
    RET.TaskQueryFailure: u"查询任务失败",
    RET.TaskNotFound: u"未查询到任务",
    RET.RestartBackendFailed: u"重启后台失败，请重试",
    RET.ModifyScanModeFailed: u"修改扫描模式失败",
    RET.GetbloodFailed: u"获取血常规信息失败",
    RET.SplitFailed: u"分裂失败",
    RET.AddCellFailed: u"添加细胞类别失败",
    RET.FavoriteCellFailed: u"收藏细胞失败，请重试",
    RET.FavoriteTaskFailed: u"收藏任务失败，请重试",
    RET.DeleteTaskFailed: u"删除任务失败",
    RET.SwitchTaskFailed: u"切换任务失败",
    RET.CellLocalizationFailure: u"细胞定位失败",
    RET.TaskListQueryFailed: u"查询任务列表失败",
    RET.TaskInfoGetFailure: u"任务信息获取失败",
    RET.CurrentTaskQueryFailed: u"查询当天任务数据失败",
    RET.PageTaskQueryFailed: u"分页查询任务数据失败",
    RET.StatisticalERR: u"统计错误",
    RET.TaskNotData: u"该任务无请求数据",
    RET.TaskNotExist: u"任务不存在",
    RET.GetRowAndColInfoFailed: u"获取行列信息失败",
    RET.GetImageInfoFailed: u"获取图片信息失败",
    RET.OrganizaInfoERR: u"组织信息出错",
    RET.TaskCellInfoQueryFailed: u"任务细胞信息查询失败",
    RET.TaskCellInfoFailed: u"任务细胞信息修改失败",
    RET.GetImageNotExist: u"图片不存在",
    RET.GetCategoryDataFailed: u"获取类别数据失败",
    RET.NotQueryInfoFound: u"未查询到信息",
    RET.ScanStartupFailed: u"扫描启动失败",
    RET.RequestScanFailed: u"请求扫描失败",
    RET.CancelScanTaskToHardwareSendFailed: u"向硬件发送取消扫描任务命令失败",
    RET.OrganizaSearchInfoFailed: u"组织检索条件失败",
    RET.ReadCopyrightInfoFailed: u"读取版权信息失败",
    RET.RemarkRecordFailed: u"备注记录失败，请重试",
    RET.ImageQualityJudgmentERR: u"图片质量判定出错",
    RET.DBCOMMITERR: u"数据库提交失败",
    RET.DBQUERYERR: u"数据库查询失败",
    RET.DBUPDATEERR: u"数据库更新失败",
    RET.ImageProcessModuleNotStarted: u"图片处理模块未启动",
    RET.ImageAnalysisModuleStartFailed: u"图片分析模块启动失败",
    RET.FileIOERR: u"文件读写错误",
    RET.FileNotExist: u"文件不存在",
    RET.FileReadFailed: u"文件读取失败",
    RET.FileLocaWriteFailed: u"写入本地文件失败",
    RET.FileCompressERR: u"文件压缩错误",
    RET.FileExportErr: u"文件导出错误",
    RET.DataTooLargePleaseReselectSearchExport: u"数据量过大，请重新选择检索条件后导出",
    RET.DataTooLargePleaseReseleDateExport: u"数据量过大，请重新选择日期后导出",
    RET.CellNumberInsufficient: u"细胞数量不足",
    RET.QCTaskCellNumberInsufficient: u"质控任务，细胞数量不足，无法做诊断。",
    RET.QCTaskInfoQueryFailed: u"质控任务信息查询失败",
    RET.StandardImageInfoQueryFailed: u"查询标准图片信息失败",
    RET.QCImageNotExist: u"质控图片不存在",
    RET.StandardImageNotExist: u"标准图片文件夹不存在",
    RET.QCTaskInfoUpdateFailed: u"更新任务质控信息失败",
    RET.SoftwareSidePleasePauseUseAndContactEngineer: u"软件端出现错误，请暂停使用并联系工程师检查",
    RET.DetectedZeroCellsUnableEvaluate: u"检测到的细胞数量为0，无法评估",
    RET.PleaseCheckHardware: u"请检查硬件情况",
    RET.AbnormalClarityQCFailed: u"清晰度异常，质控未通过",
    RET.TemperatureHigh: u"设备内部温度过高，请注意使用环境。",
    RET.OilLowNoScan: u"油量已耗尽，不可进行扫描工作，请更换油袋。",
    RET.NoHardware: u"硬件扫描仪未连接",
    RET.SlideNotRecognizedTaskCreatFailed: u"未识别到玻片，本次任务创建失败",
    RET.ScanErr: u"扫描过程中故障，结果不可用，请重新扫描",
    RET.CreateScanTaskFailed: u"创建扫描任务失败，请重试",
    RET.CreateTaskFailed: u"创建任务失败",
    RET.WhiteCellClassCountFailed: u"白细胞分类计数失败，请重新扫描",
    RET.PlateletAnalysisFailed: u"血小板分析失败，请重新扫描",
    RET.PlateletCountAnalysisFailed: u"血小板计数分析失败，请重新扫描",
    RET.RedCellAnalysisFailed: u"红细胞分析失败，请重新扫描",
    RET.QueryParameterTableFailed: u"查询参数表失败",
    RET.QueryCriteriaSpecialChar: u"查询条件中含有特殊字符",
    RET.QueryPatientNameERR: u"查询患者名字出错",
    RET.QueryPatientInfoERR: u"查询患者信息出错",
    RET.QueryCurrentSystemVersionFailed: u"查询当前系统版本失败",
    RET.QuerySystemInfoFailed: u"查询系统设置信息失败",
    RET.SystemInfoSaveFailed: u"系统信息保存失败",
    RET.QueryRuleSettingInfoFailed: u"查询规则设置信息失败",
    RET.RuleSettingInfoSaveFailed: u"规则设置信息保存失败",
    RET.RecordUserLoginInfoFailed: u"记录用户登录状态信息失败",
    RET.ChangeUserLoginInfoFailed: u"更改用户登录状态信息失败",
    RET.QCReportNotViewedOrModify: u"质控报告已生成，不允许再次查看、修改",
    RET.GetReportFailed: u"获取报告失败",
    RET.ModifReportFailed: u"修改报告失败",
    RET.ReportInfoQueryFailed: u"报告信息查询失败",
    RET.PrintingException: u"打印异常，请重试",

    RET.GetCurrentLanguageFailed: u"获取当前语言失败",
    RET.CreateDefaultLanguageFailed: u"创建默认语言记录失败",
    RET.GetCurrentVersionFailed: u"获取当前版本配置失败",
    RET.ParseSelectLanguagesFailed: u"解析 select_languages 失败",
    RET.GetLanguageInfoFailed: u"获取语言信息失败",
    RET.GetLanguageRecordFailed: u"获取当前语言记录失败",
    RET.LanguageNotAllowed: u"语言不在允许的列表中",
    RET.UpdateLanguageFailed: u"更新语言记录失败",
    RET.SetLanguageFailed: u"设置语言失败",

    RET.GetThresholdsDataFailed: u"获取阈值数据失败",
    RET.NoThresholdsFound: u"未找到相应阈值",
    RET.GetThresholdsInfoFailed: u"获取阈值信息失败",
    RET.AddThresholdsFailed: u"添加阈值失败",
    RET.UpdateThresholdsFailed: u"更新阈值失败",
    RET.SetThresholdsFailed: u"设置阈值失败",

    RET.GetVersionConfigFailed: u"获取版本配置失败",
    RET.CreateVersionConfigFailed: u"创建版本配置失败",
    RET.VersionNotFound: u"版本未找到",
    RET.UpdateVersionInfoFailed: u"更新版本信息失败",
    RET.SetCurrentVersionFailed: u"设置当前版本失败",
    RET.GetVersionInfoFailed: u"获取版本信息失败",
    RET.CurrentVersionNotSet: u"当前版本未设置",
    RET.SetVersionInfoFailed: u"设置版本信息失败",

    RET.DBUpdateError: u"数据库备份失败",
    RET.DBQueryError: u"导出数据库失败",
    RET.TaskExportError: u"导出任务数据失败",
    RET.TaskAddError: u"后台任务添加失败",
    RET.TaskDBExportError: u"导出任务DB数据库失败",
    RET.TaskDBOperationError: u"导出任务DB数据库操作失败",
    RET.TaskExportFailure: u"导出任务失败",

    RET.GetUaxisCodeFailed: u"获取U轴报警代码失败",
    RET.GetSysCodeFailed: u"获取系统运行代码失败",
    RET.GetHardwareStatusFailed: u"获取硬件模块状态失败",
    RET.ProcessHardwareStatusDataFailed: u"处理硬件状态数据失败",

    RET.GetPythonLogFilesFailed: u"获取 Python 日志路径下文件失败",
    RET.GetProductLogFilesFailed: u"获取 Product 日志路径下文件失败",
    RET.GetGoLogFilesFailed: u"获取 Go 日志路径下文件失败",
    RET.GetPythonLogFileListFailed: u"获取 Python 日志文件列表失败",
    RET.GetProductLogFileListFailed: u"获取 Product 日志文件列表失败",
    RET.GetGoLogFileListFailed: u"获取 Go 日志文件列表失败",
    RET.ReadLogFileFailed: u"日志文件读取失败",
    RET.FileCompressFailed: u"文件压缩失败",
    RET.LogModuleTypeError: u"日志类型错误",
    RET.FileDownloadFailed: u"文件下载错误",
    RET.LogFilterFailed: u"日志筛选失败",
    RET.TimeFormatError: u"时间信息格式错误",
    RET.SaveHardwareLogFailed: u"保存硬件日志信息失败",
    RET.InvalidModuleTypeError: u"无效的模块类型",
    RET.LogPaginationError: u"分页日志信息失败",
    RET.LogFilePathError: u"日志文件夹路径错误",
    RET.QueryLogInfoFailed: u"日志信息查询失败",

    RET.SysStatusQueryFailed: u"查询系统状态失败",
    RET.SensorStatusQueryFailed: u"查询传感器状态失败",
    RET.TopCommandQueryFailed: u"top查询失败",
    RET.NvidiaCommandQueryFailed: u"nvidia-smi查询失败",
    RET.PythonServerQueryFailed: u"查询Python服务器状态失败",
    RET.GoServerQueryFailed: u"查询Go服务器状态失败",
    RET.DiskInfoQueryFailed: u"查询磁盘信息失败",
    RET.MemoryInfoQueryFailed: u"查询内存信息失败",
    RET.InternalStorageQueryFailed: u"查询内部存储信息失败",
    RET.CpuInfoQueryFailed: u"查询CPU信息失败",
    RET.GpuInfoQueryFailed: u"查询GPU信息失败",
    RET.SystemStatusQueryFailed: u"获取系统失败",


}


# 硬件错误信息状态码及描述
HARDWARE_ERR_CODE = {

    "4200": "玻片相机故障",
    "4201": "进片仓门超时未关闭",
    "4202": "进样仓有玻片放反",
    "4203": "出片仓门超时未关闭",
    "4300": "通信故障（下位机软件与设备）",
    "4301": "通信故障（下位机与golang模块redis通信）",
    "4400": "多片检测相机1故障",
    "4401": "舵机故障",  # 进样缓存舵机故障
    "4402": "舵机故障",  # 出样缓存舵机故障
    "4403": "舵机故障",  # 玻片舵机故障
    "4404": "电机故障",  # 2号电机故障（水平轴）
    "4405": "电机故障",  # 3号电机故障（竖直轴）
    "4406": "电机故障",  # 4号电机故障（旋转轴）
    "4407": "电机故障",  # 6号电机故障（X轴）
    "4408": "电机故障",  # 7号电机故障（Y轴）
    "4409": "电机故障",  # 8号电机错误（L轴）
    "4410": "电机故障",  # 9号电机错误（音圈）
    "4411": "进片仓门开启故障",
    "4412": "出片仓门开启故障",
    "4413": "故障恢复失败，不再尝试恢复，请联系售后",
    "4414": "系统自检失败",
    "4415": "扫描光路故障",

}

# 提示消息类别
INFO_TYPE = {
    "1": "提示信息",
    "2": "警告信息",
    "3": "错误信息",
    "4": "停用信息",
}
