from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.orm.models import SimulationData
from app.db.pg_con import get_db
from app.schemas.schemas_engineer import ConfigModel, SearchRequest, ExportRequest, BackupRequest


class TestServer:

    @staticmethod  # 无需实例化对象
    def get_hide(db: Session):
        result = {
            "errno": "0",
            "errmsg": 'Success',
            "data": {
                "mark_data": True,
                "mark_file": True,
            }
        }
        new_simulation = SimulationData(
            get_hide=result
        )
        db.add(new_simulation)
        db.commit()
        db.refresh(new_simulation)

        return result

    @staticmethod
    async def config(db: Session):
        data = {
            "errno": "0",
            "errmsg": '成功',
        }

        new_simulation = SimulationData(
            config=data
        )
        db.add(new_simulation)
        db.commit()
        db.refresh(new_simulation)

        return data

    @staticmethod
    async def search_data(request: SearchRequest, db: Session):
        response_data = {
            "current_page": request.current_page,
            "task_info_dict_list": [
                {
                    "ID": None,
                    "box_slot": "001-7",
                    "create_time": "2024-08-07 13:00",
                    "failed_reason": None,
                    "finish_time": "2024-08-07 13:17",
                    "is_audit": False,
                    "is_deleted_image": False,
                    "is_error": [],
                    "is_favorite": False,
                    "is_flatness": True,
                    "is_save": False,
                    "is_slide_out": False,
                    "patient_id": 5736,
                    "patient_info": {
                        "age": None,
                        "application_date": "2024-08-07",
                        "application_id": None,
                        "application_time": "13:00:20",
                        "bed_id": None,
                        "case_no": None,
                        "department": None,
                        "gender": None,
                        "inspect_doc_name": None,
                        "notes": None,
                        "patient_id": 5736,
                        "patient_name": "",
                        "patient_type": None,
                        "pay_type": None,
                        "sample_type": None,
                        "slide_id": "2032688545",
                        "slide_slot": "001-7",
                        "submission_doc_name": "",
                        "verify_doc_name": None
                    },
                    "patient_name": "",
                    "quality_percent": 0.2869540873460246,
                    "scan_parameter": None,
                    "scan_result": "-",
                    "scan_type": "All",
                    "slide_id": "2032688545",
                    "slide_slot": "001-7",
                    "status": "Success",
                    "task_id": 5736,
                    "ustretching_too_much": False
                },
                {
                    "ID": None,
                    "box_slot": "001-6",
                    "create_time": "2024-08-07 12:36",
                    "failed_reason": None,
                    "finish_time": "2024-08-07 12:59",
                    "is_audit": False,
                    "is_deleted_image": False,
                    "is_error": [
                        "玻片号读取失败，请手动录入信息"
                    ],
                    "is_favorite": False,
                    "is_flatness": True,
                    "is_save": False,
                    "is_slide_out": False,
                    "patient_id": 5735,
                    "patient_info": {
                        "age": None,
                        "application_date": "2024-08-07",
                        "application_id": None,
                        "application_time": "12:36:29",
                        "bed_id": None,
                        "case_no": None,
                        "department": None,
                        "gender": None,
                        "inspect_doc_name": None,
                        "notes": None,
                        "patient_id": 5735,
                        "patient_name": "",
                        "patient_type": None,
                        "pay_type": None,
                        "sample_type": None,
                        "slide_id": "2032688544",
                        "slide_slot": "001-6",
                        "submission_doc_name": "",
                        "verify_doc_name": None
                    },
                    "patient_name": "",
                    "quality_percent": 0.2893415689469175,
                    "scan_parameter": None,
                    "scan_result": "-",
                    "scan_type": "All",
                    "slide_id": "2032688544",
                    "slide_slot": "001-6",
                    "status": "Success",
                    "task_id": 5735,
                    "ustretching_too_much": False
                }
            ],
            "total_count": 2,
            "errmsg": "OK",
            "errno": "0"
        }

        new_simulation = SimulationData(
            data_search=response_data,
        )
        db.add(new_simulation)
        db.commit()
        db.refresh(new_simulation)

        return response_data

    @staticmethod
    def export_data(request: ExportRequest):
        # 根据 type 和 task_ids 参数生成响应数据
        if request.type == "task" and request.task_ids:
            # 这里可以根据实际情况处理任务ID
            response_data = {
                "errmsg": "导出任务DB数据库失败",
                "errno": "4009"
            }
        else:
            response_data = {
                "errmsg": "参数错误",
                "errno": "4000"
            }

        return response_data

    @staticmethod
    def get_back(request: BackupRequest, db: Session):
        # 根据 type 参数生成响应数据
        if request.type == "sql":
            response_data = {
                "data": {
                    "dst_path": "/home/xiaoying/Downloads"
                },
                "errmsg": "成功",
                "errno": "0"
            }
        else:
            response_data = {
                "data": {},
                "errmsg": "类型错误",
                "errno": "1"
            }
        new_simulation = SimulationData(
            data_backup=response_data  # 保存 response_data 到 data_backup 字段
        )

        # 添加到数据库会话并提交
        db.add(new_simulation)
        db.commit()

        return response_data
