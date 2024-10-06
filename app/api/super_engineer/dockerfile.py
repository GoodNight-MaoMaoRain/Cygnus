from fastapi import UploadFile
from typing import List
from app.schemas.schemas_super_engineer import UploadResponse
from app.common.response_code import RET
from fastapi_babel.core import _

class DockerfileAPI:
    async def upload_dockerfile(self, files: List[UploadFile]) -> dict:
        # 处理上传文件内容，而不是保存到本地
        for file in files:
            content = await file.read()  # 读取文件内容，可以进一步处理

        # 返回文件信息，不需要保存到本地
        return {
            "errno": RET.OK,
            "errmsg": _("上传成功"),
            "filename": files[0].filename,
            "content_type": files[0].content_type
        }

import os.path
import time
from fastapi import APIRouter, UploadFile, File, Form
from app.api.super_engineer import settings
from app.common.response_code import RET

router = APIRouter()


# 文件上传接口
@router.post('/upload_big_file')
async def upload_big_file(
        file: UploadFile = File(...),
        chunknumber: str = Form(...,description='序号'),
        identifier: str = Form(...,description='文件唯一标识符')
):
    if len(chunknumber) == 0 or len(identifier) == 0:
        return {"error": "没有传递相关参数"}

    task = identifier  # 获取文件唯一标识符
    chunk = chunknumber  # 获取该分片在所有分片中的序号【客户端设定】
    filename = '%s%s' % (task, chunk)  # 构成该分片的唯一标识符

    # 确保上传目录存在
    upload_dir = os.path.join(settings.STATIC_DIR, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    contents = await file.read()  # 异步读取文件
    with open(f'{settings.STATIC_DIR}/uploads/{filename}', 'wb') as f:
        f.write(contents)

    return {"errno": RET.OK, "filename": filename}


@router.post("/upload/mergefile")
async def mergefile(
        identifier: str = Form(..., description='获取文件的唯一标识符'),
        filename: str = Form(..., description='获取上传文件的文件名'),
        chunkstar: int = Form(...),
):
    if len(filename) == 0 or len(identifier) == 0:
        return {"errno": "没有传递相关参数"}

    target_filename = filename  # 获取上传文件的文件名【保存的文件名】
    task = identifier  # 获取文件的唯一标识符
    chunk = chunkstar  # 分片序号开始的默认序号=0

    if os.path.isfile(f'{settings.STATIC_DIR}/uploads/{target_filename}'):  # 如果客户端传递过来的文件名在服务器上已经存在，那么另外新建一个【时间戳.后缀名】文件
        t = time.time()  # 时间戳
        timeUnix = str(round(t * 1000))  # 毫秒级时间戳
        filesuffix = os.path.splitext(target_filename)[1]  # 后缀名
        target_filename = timeUnix + filesuffix  # 新文件名【时间戳，后缀名】

    error_i = 0
    chunkfilename = ""

    with open(f"{settings.STATIC_DIR}/uploads/{target_filename}", 'wb') as target_file:  # 创建新文件
        while True:  # 循环把分片文件写入新建的文件
            if os.path.isfile(f"{settings.STATIC_DIR}/uploads/{task}{chunk}"):  # 存到这个文件
                try:
                    # 分片文件名
                    chunkfilename = f"{settings.STATIC_DIR}/uploads/{task}{chunk}"
                    # 按序打开每个分片
                    with open(chunkfilename, 'rb') as source_file:
                        # 读取分片内容写入到新文件
                        target_file.write(source_file.read())
                except IOError:  # 当分片标志chunk累加到最后，文件夹里面不存在{task}{chunk}文件时，退出循环
                    break
                os.remove(f"{settings.STATIC_DIR}/uploads/{task}{chunk}")  # 删除分片文件
            else:  # 【如果分片文件上传中途出错，导致中间缺少某个分片文件，跳过它，不退出循环，直到累计缺少次数大于3次，再跳出循环】
                error_i += 1
                if error_i > 3:
                    break
            chunk += 1

    os.chmod(f"{settings.STATIC_DIR}/uploads/{target_filename}", 0o664)  # linux设置权限0o664、0o400
    return {"errno": RET.OK, "filename": f"{settings.STATIC_DIR}/uploads/{target_filename}"}
