import shutil
import librosa

from fastapi import APIRouter, Request

from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter
from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudioFilter, ObjSoundFusionAudio
from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.service.sound_fusion.sound_fusion_service import SoundFusionService
from server.util.util import str_to_int, save_file

router = APIRouter(prefix="/fusion")


@router.post("/get_sound_fusion_audio")
async def get_sound_fusion_audio(request: Request):
    form_data = await request.form()
    audio_filter = ObjSoundFusionAudioFilter(form_data)

    count = SoundFusionService.find_count(audio_filter)
    audio_list = SoundFusionService.find_list(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/batch_add_sound_fusion_audio")
async def batch_add_sound_fusion_audio(request: Request):
    form_data = await request.form()
    ref_audio_ids = form_data.get('refAudioIds')
    ref_audio_list = ReferenceAudioService.find_list(ObjReferenceAudioFilter({'audio_ids_str': ref_audio_ids}))
    if ref_audio_list is None and len(ref_audio_list) <= 0:
        return ResponseResult(code=1, msg='音频不存在')

    sound_fusion_audio_list = []

    for audio in ref_audio_list:
        new_path = SoundFusionService.get_new_sound_fusion_path()
        shutil.copy2(audio.audio_length, new_path)
        sound = ObjSoundFusionAudio(
            role_name=db_config.role_name, audio_name=audio.audio_name, audio_path=audio.audio_path,
            content=audio.content,
            language=audio.language, category=audio.category, audio_length=new_path
        )
        sound_fusion_audio_list.append(sound)

    SoundFusionService.batch_add_sound_fusion_audio(sound_fusion_audio_list)
    return ResponseResult()


@router.post("/add_sound_fusion_audio")
async def add_sound_fusion_audio(request: Request):
    form_data = await request.form()

    file = form_data.get('file')

    audio = ObjSoundFusionAudio(
        role_name=form_data.get('roleName'),
        audio_name=form_data.get('audioName'),
        # audio_path=form_data.get('audioPath'),
        content=form_data.get('content'),
        language=form_data.get('language'),
        category=form_data.get('category'),
        # audio_length=form_data.get('audioLength'),
        remark=form_data.get('remark')
    )

    new_path = SoundFusionService.get_new_sound_fusion_path()

    save_file(file, new_path)

    audio.audio_path = new_path

    # 直接计算音频文件的时长（单位：秒）
    audio.audio_length = librosa.get_duration(filename=new_path)

    SoundFusionService.add_sound_fusion_audio(audio)
    return ResponseResult()


@router.post("/update_sound_fusion_audio")
async def update_sound_fusion_audio(request: Request):
    form_data = await request.form()
    audio = ObjSoundFusionAudio(
        id=str_to_int(form_data.get('id'), 0),
        role_name=form_data.get('roleName'),
        audio_name=form_data.get('audioName'),
        # audio_path=form_data.get('audioPath'),
        content=form_data.get('content'),
        language=form_data.get('language'),
        category=form_data.get('category'),
        # audio_length=form_data.get('audioLength'),
        remark=form_data.get('remark')
    )

    if audio.id <= 0:
        return ResponseResult(code=1, msg='音频Id异常')

    SoundFusionService.update_sound_fusion_audio(audio)

    return ResponseResult()


@router.post("/delete_sound_fusion_audio")
async def delete_sound_fusion_audio(request: Request):
    form_data = await request.form()
    audio_id = str_to_int(form_data.get('audioId'), 0)
    if audio_id <= 0:
        return ResponseResult(code=1, msg='音频Id异常')

    SoundFusionService.delete_sound_fusion_audio_by_id(audio_id)

    return ResponseResult()
