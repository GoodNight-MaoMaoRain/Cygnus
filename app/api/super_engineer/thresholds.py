import traceback
from loguru import logger
from app.crud.crud_threshold import CRUDAlgorithmThresholds, CRUDStretchingThresholds
from app.schemas.schemas_super_engineer import AlgorithmThresholds, StretchingThresholds
from app.common.response_code import RET
from fastapi_babel.core import _


class StretchingThresholdsAPI:
    def __init__(self, crud: CRUDStretchingThresholds):
        self.crud = crud

    def get_stretching_thresholds(self) -> dict:
        try:
            logger.info("开始查询当前不舒展阈值信息")
            # 从数据库中获取不舒展阈值信息
            try:
                stretching_thresholds = self.crud.get_stretching_thresholds()
                logger.info(f"获取到的不舒展阈值数据: {stretching_thresholds}")
            except Exception:
                errmsg = f'获取不舒展阈值数据失败: {traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.GetThresholdsDataFailed, "errmsg": _("获取不舒展阈值数据失败"), "data": {}}

            if not stretching_thresholds:
                errmsg = f'未查询相应阈值，请查看数据库是否有对应信息：{traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.NoThresholdsFound, "errmsg": _("未查询相应不舒展阈值，请查看数据库是否有对应信息"),
                        "data": {}}

            # 数据库模型映射到 Schema 中
            stretching_thresholds_data = StretchingThresholds(
                StretchingSize=stretching_thresholds.stretching_size
            )

            # 返回成功的响应，包含阈值
            logger.info("获取不舒展阈值成功")
            return {"errno": RET.OK, "errmsg": _("获取不舒展阈值信息成功"),
                    "data": stretching_thresholds_data.model_dump()}

        except Exception:
            errmsg = f'获取不舒展阈值失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.GetThresholdsInfoFailed, "errmsg": _("获取不舒展阈值失败"), "data": {}}

    def set_stretching_thresholds(self, new_stretching_thresholds: StretchingThresholds):
        try:
            logger.info("开始设置当前不舒展阈值信息")
            # 数据库拿数据
            try:
                stretching_thresholds = self.crud.get_stretching_thresholds()
                logger.info(f'当前不舒展阈值数据为: {stretching_thresholds}')
            except Exception:
                errmsg = f'获取不舒展阈值失败: {traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.GetThresholdsDataFailed, "errmsg": _("获取不舒展阈值数据失败"), "data": {}}

            # 创建新实例对象 此时数据库的默认值会自动填充进去
            if not stretching_thresholds:
                try:
                    self.crud.create_stretching_thresholds()
                    logger.info("创建新的不舒展阈值成功")
                except Exception:
                    errmsg = f'创建不舒展阈值失败: {traceback.format_exc()}'
                    logger.error(errmsg)
                    return {"errno": RET.AddThresholdsFailed, "errmsg": _("添加不舒展阈值失败"), "data": {}}

            # 提交更新到数据库
            try:
                # 获取新的阈值字段进行映射，匹配数据库字段  如果此时字段相同可以 自动匹配 exclude_unset=True
                new_value = {
                    'stretching_size': new_stretching_thresholds.StretchingSize,
                }

                self.crud.update_stretching_thresholds(stretching_thresholds, new_value)
                logger.info('不舒展阈值记录更新成功')
            except Exception:
                errmsg = f'不舒展阈值记录更新失败:{traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.UpdateThresholdsFailed, "errmsg": _("不舒展阈值更新失败"), "data": {}}

            stretching_thresholds_data = StretchingThresholds(
                StretchingSize=stretching_thresholds.stretching_size
            )

            # 返回成功的响应，并包含更新后的阈值数据
            logger.info("不舒展阈值记录设置成功")
            return {"errno": RET.OK, "errmsg": _("不舒展阈值记录设置成功"), "data": stretching_thresholds_data.model_dump()}

        except Exception:
            errmsg = f"设置不舒展阈值失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.SetThresholdsFailed, "errmsg": _("设置不舒展阈值失败"), "data": {}}







class AlgorithmThresholdsAPI:
    def __init__(self, crud: CRUDAlgorithmThresholds):
        # 初始化 CRUD 操作对象
        self.crud = crud

    def get_thresholds(self) -> dict:
        try:
            logger.info("开始查询当前算法阈值信息")
            # 从数据库中获取阈值信息
            try:
                thresholds = self.crud.get_algorithm_thresholds()
                logger.info(f"获取到的算法阈值数据: {thresholds}")
            except Exception:
                errmsg = f"获取算法阈值数据失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetThresholdsDataFailed, "errmsg": _("获取算法阈值数据失败"), "data": {}}

            # 检查是否找到阈值
            if not thresholds:
                errmsg = '未查询相应阈值，请查看数据库是否有对应信息'
                logger.error(errmsg)
                return {"errno": RET.NoThresholdsFound, "errmsg": _("未查询相应算法阈值，请查看数据库是否有对应信息"),
                        "data": {}}

            # 将数据库模型中的阈值数据映射到 Schema 对象中
            thresholds_data = AlgorithmThresholds(
                WhiteSize=thresholds.white_size,
                RedSize=thresholds.red_size,
                PCSize=thresholds.pc_size,
                ThinkSize=thresholds.thick_size,
                PlateletSize=thresholds.platelet_size,
                MicroSize=thresholds.micro_size
            )

            # 返回成功的响应，并包含阈值数据
            logger.info("获取算法阈值信息成功")
            return {"errno": RET.OK, "errmsg": _("获取算法阈值信息成功"), "data": thresholds_data.model_dump()}

        except Exception:
            errmsg = f"获取阈值信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GetThresholdsInfoFailed, "errmsg": _("获取算法阈值信息失败"), "data": {}}

    def set_thresholds(self, new_thresholds: AlgorithmThresholds) -> dict:
        try:
            logger.info("开始获取数据库算法阈值信息")
            # 从数据库中获取当前的阈值信息
            try:
                thresholds = self.crud.get_algorithm_thresholds()
                logger.info(f"当前算法阈值数据: {thresholds}")
            except Exception:
                errmsg = f"获取算法阈值数据失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetThresholdsDataFailed, "errmsg": _("获取算法阈值数据失败"), "data": {}}

            # 如果当前数据库中没有阈值数据，则创建一个新的 Threshold 实例
            if not thresholds:
                try:
                    self.crud.create_algorithm_thresholds()  # 添加到数据库
                    logger.info("创建新的算法阈值记录成功")
                except Exception:
                    errmsg = f"添加算法阈值失败: {traceback.format_exc()}"
                    logger.error(errmsg)
                    return {"errno": RET.AddThresholdsFailed, "errmsg": _("添加算法阈值失败"), "data": {}}

            # 提交更新操作到数据库
            try:
                # 获取新的阈值数据并进行字段映射
                new_values = {
                    'white_size': new_thresholds.WhiteSize,
                    'red_size': new_thresholds.RedSize,
                    'pc_size': new_thresholds.PCSize,
                    'thick_size': new_thresholds.ThinkSize,
                    'platelet_size': new_thresholds.PlateletSize,
                    'micro_size': new_thresholds.MicroSize
                }

                self.crud.update_algorithm_thresholds(thresholds, new_values)
                logger.info("算法阈值记录更新成功")
            except Exception:
                errmsg = f"更新阈值失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.UpdateThresholdsFailed, "errmsg": _("算法更新阈值失败"), "data": {}}

            # 将更新后的数据映射到 Schema 对象中
            thresholds_data = AlgorithmThresholds(
                WhiteSize=thresholds.white_size,
                RedSize=thresholds.red_size,
                PCSize=thresholds.pc_size,
                ThinkSize=thresholds.thick_size,
                PlateletSize=thresholds.platelet_size,
                MicroSize=thresholds.micro_size
            )

            # 返回成功的响应，并包含更新后的阈值数据
            logger.info("设置算法阈值成功")
            return {"errno": RET.OK, "errmsg": _("修改成功"), "data": thresholds_data.model_dump()}

        except Exception:
            errmsg = f"设置算法阈值失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.SetThresholdsFailed, "errmsg": _("设置算法阈值失败"), "data": {}}
