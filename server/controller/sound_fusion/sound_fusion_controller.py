from fastapi import APIRouter, Request

from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudioFilter
from server.common.response_result import ResponseResult
from server.service.sound_fusion.sound_fusion_service import SoundFusionService

router = APIRouter(prefix="/fusion")


@router.post("/get_sound_fusion_audio")
async def get_sound_fusion_audio(request: Request):
    form_data = await request.form()
    audio_filter = ObjSoundFusionAudioFilter(form_data)

    count = SoundFusionService.find_count(audio_filter)
    audio_list = SoundFusionService.find_whole_list(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/batch_add_sound_fusion_audio")
async def batch_add_sound_fusion_audio(request: Request):
    form_data = await request.form()
    ref_audio_ids = form_data.get('refAudioIds')
    

    return ResponseResult()


@router.post("/add_sound_fusion_audio")
async def add_sound_fusion_audio(request: Request):
    form_data = await request.form()

    return ResponseResult()


@router.post("/update_sound_fusion_audio")
async def update_sound_fusion_audio(request: Request):
    form_data = await request.form()

    return ResponseResult()


@router.post("/delete_sound_fusion_audio")
async def delete_sound_fusion_audio(request: Request):
    form_data = await request.form()

    return ResponseResult()
