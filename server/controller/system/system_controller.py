from fastapi import APIRouter, Request

from server.bean.system.role import Role
from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.system.system_service import SystemService
from server.util.util import ValidationUtils

router = APIRouter(prefix="/system")


@router.post("/load_last_role_name")
async def load_last_role_name():
    role = SystemService.get_valid_role()

    role_list = SystemService.get_role_list()

    return ResponseResult(data={
        "role": role,
        "roleList": role_list
    })


@router.post("/switch_role_workspace")
async def switch_role_workspace(request: Request):
    form_data = await request.form()
    role_name = form_data.get("roleName")
    role_category = form_data.get("roleCategory")
    if ValidationUtils.is_empty(role_name):
        return ResponseResult(code=1, msg="roleName is empty")
    if ValidationUtils.is_empty(role_category):
        return ResponseResult(code=1, msg="roleCategory is empty")
    role = Role(category=role_category, name=role_name)
    db_config.update_db_path(role)
    SystemService.update_sys_cache('system', 'role', role.to_json_string())
    return ResponseResult(code=0, msg="success")
