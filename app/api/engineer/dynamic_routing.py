from fastapi import HTTPException, status
from sqlalchemy import null

from app.api.auth2.jwt import SECRET_KEY, ALGORITHM
from app.orm.models import UserRole
import bcrypt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Dict
from app.orm.models import SimulationData


# # 生成固定密码的哈希值
# hashed_password = hash_password("123456")
# print(hashed_password)

# 加密函数
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# 函数密码比较   明文和数据库中的哈希直接对比
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def authenticate_user(db: Session, user_name: str, password: str) -> UserRole:
    """认证用户"""
    user = db.query(UserRole).filter(UserRole.username == user_name).first()
    print(user)
    # 先判断数据库中是否有user 当为True时抛出异常，当有的时候将密码交给verify_password判断，两者都为False返回user
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return user


def get_engineer_routes():
    """返回工程师的动态路由"""
    return {
        "errno": "0",
        "errmsg": "成功",
        "success": null,
        "data": [
            {
                "path": "/logManagement",
                "name": "logManagement",
                "meta": {
                    "title": "日志管理",
                    "icon": "tdesign:catalog",
                    "rank": 1
                }
            },
            {
                "path": "/systemInspection",
                "name": "systemInspection",
                "meta": {
                    "title": "系统质检",
                    "icon": "material-symbols:browse-activity-outline-rounded",
                    "rank": 2
                }
            },
            {
                "path": "/dataManagement",
                "name": "dataManagement",
                "meta": {
                    "title": "数据管理",
                    "icon": "iconoir:database-settings",
                    "rank": 3
                }
            },
            {
                "path": "/configuration",
                "meta": {
                    "title": "系统配置",
                    "icon": "tdesign:system-setting",
                    "rank": 4
                },
                "children": [
                    {
                        "path": "/factorySettings",
                        "name": "factorySettings",
                        "meta": {
                            "title": "出厂设置"
                        }
                    },
                    {
                        "path": "/softwareConfiguration",
                        "name": "softwareConfiguration",
                        "meta": {
                            "title": "软件配置"
                        }
                    },
                    {
                        "path": "/algorithmConfiguration",
                        "name": "algorithmConfiguration",
                        "meta": {
                            "title": "算法配置"
                        }
                    }
                ]
            },
            {
                "path": "/versionInformation",
                "name": "versionInformation",
                "meta": {
                    "title": "版本信息",
                    "icon": "tdesign:system-setting",
                    "rank": 5
                }
            }
        ]
    }


def get_super_engineer_routes(db: Session):
    """返回超级工程师的动态路由"""
    data = {
        "errno": "0",
        "errmsg": "成功",
        "success": "null",
        "data": [
            {
                "path": "/logManagement",
                "name": "logManagement",
                "meta": {
                    "title": "日志管理",
                    "icon": "tdesign:catalog",
                    "rank": 1
                }
            },
            {
                "path": "/systemInspection",
                "name": "systemInspection",
                "meta": {
                    "title": "系统质检",
                    "icon": "material-symbols:browse-activity-outline-rounded",
                    "rank": 2
                }
            },
            {
                "path": "/dataManagement",
                "name": "dataManagement",
                "meta": {
                    "title": "数据管理",
                    "icon": "iconoir:database-settings",
                    "rank": 3
                }
            },
            {
                "path": "/configuration",
                "meta": {
                    "title": "系统配置",
                    "icon": "tdesign:system-setting",
                    "rank": 4
                },
                "children": [
                    {
                        "path": "/factorySettings",
                        "name": "factorySettings",
                        "meta": {
                            "title": "出厂设置"
                        }
                    },
                    {
                        "path": "/softwareConfiguration",
                        "name": "softwareConfiguration",
                        "meta": {
                            "title": "软件配置"
                        }
                    },
                    {
                        "path": "/algorithmConfiguration",
                        "name": "algorithmConfiguration",
                        "meta": {
                            "title": "算法配置"
                        }
                    }
                ]
            },
            {
                "path": "/versionInformation",
                "name": "versionInformation",
                "meta": {
                    "title": "版本信息",
                    "icon": "tdesign:system-setting",
                    "rank": 5
                }
            }
        ]
    }

    # new_simulation = SimulationData(
    #     async_router=data
    # )
    # db.add(new_simulation)
    # db.commit()
    # db.refresh(new_simulation)

    return data


def get_routes_based_on_role(role_id: int,db: Session):
    """根据用户角色返回路由"""
    if role_id == -1:  # engineer
        return get_engineer_routes()
    elif role_id == -2:  # super_engineer
        return get_super_engineer_routes(db)
    else:
        return {"errno": "1", "errmsg": "无效的角色权限"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
