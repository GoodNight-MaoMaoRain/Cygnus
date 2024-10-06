import base64
import traceback
from loguru import logger
from app.common.response_code import RET
from fastapi_babel.core import _
from app.lib.hardware.hardware.client import HttpClient


# 用于管理和获取二维码相机拍照图片的控制器
class CameraPictureController:
    __instance = None

    @staticmethod
    def get_instance():
        if CameraPictureController.__instance is None:
            CameraPictureController.__instance = CameraPictureController()
        return CameraPictureController.__instance

    def get_QRcamera_picture(self):
        """
            获取下位机二维码相机拍照图片
        """
        try:
            logger.info('请求下位机二维码相机拍照图片')
            img_response = HttpClient.get_instance().query_QRcamera_picture()
            logger.info(f'接口返回: {img_response}')

            if img_response is None:
                errmsg = '下位机二维码相机拍照图片失败: 接口返回了 None'
                logger.error(errmsg)
                return {"errno": RET.GetImageInfoFailed, "errmsg": _("下位机二维码相机拍照图片失败")}

            img = img_response.get('photoData')

            if img:
                logger.info('成功获取到图片数据')
                QRcamera_picture_status = {
                    "QRcameraPhoto": img.encode(),
                }
            else:
                errmsg = '下位机二维码相机拍照图片失败: 图片数据为空'
                logger.error(errmsg)
                return {"errno": RET.GetImageInfoFailed, "errmsg": _("下位机二维码相机拍照图片失败")}

        except Exception:
            errmsg = f'下位机二维码相机拍照图片失败: {str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.GetImageInfoFailed, "errmsg": _("下位机二维码相机拍照图片失败")}

        if QRcamera_picture_status:
            try:
                data = {}
                QRcameraPhotobase64 = base64.b64encode(QRcamera_picture_status.get("QRcameraPhoto")).decode('utf8')
                data["QRcameraPhoto"] = QRcameraPhotobase64
                return {"errno": RET.OK, "errmsg": "成功", "data": data}

            except Exception:
                errmsg = f'图片数据转换为 Base64 失败: {str(traceback.format_exc())}'
                logger.error(errmsg)
                return {"errno": RET.GetImageInfoFailed, "errmsg": _("图片数据转换为 Base64 失败")}

        else:
            errmsg = '下位机二维码相机拍照图片失败: 图片数据为空'
            logger.error(errmsg)
            return {"errno": RET.GetImageInfoFailed, "errmsg": _("下位机二维码相机拍照图片失败")}
