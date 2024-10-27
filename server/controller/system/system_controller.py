from fastapi import APIRouter, Request

from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.system.system_service import SystemService
from server.util.util import ValidationUtils

router = APIRouter(prefix="/system")


@router.post("/load_last_role_name")
async def load_last_role_name():
    role_name = SystemService.get_valid_role_name()

    role_list = SystemService.get_role_list()

    return ResponseResult(data={
        "roleName": role_name,
        "roleList": role_list
    })


@router.post("/switch_role_workspace")
async def switch_role_workspace(request: Request):
    form_data = await request.form()
    role_name = form_data.get("roleName")
    if ValidationUtils.is_empty(role_name):
        return ResponseResult(code=1, msg="roleName is empty")
    db_config.update_db_path(role_name)
    SystemService.update_sys_cache('system', 'roleName', role_name)
    return ResponseResult(code=0, msg="success")
