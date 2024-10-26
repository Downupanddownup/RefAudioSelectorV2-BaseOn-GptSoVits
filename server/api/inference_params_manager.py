from server.util.util import str_to_int, str_to_float


class InferenceParams:
    def __init__(self, refer_wav_path: str = None, prompt_text: str = None
                 , prompt_language: str = None, cut_punc: str = None
                 , top_k: int = None, top_p: float = None, temperature: float = None, speed: float = None):
        self.refer_wav_path = refer_wav_path
        self.prompt_text = prompt_text
        self.prompt_language = prompt_language
        self.cut_punc = cut_punc
        self.top_k = str_to_int(top_k, None)
        self.top_p = str_to_float(top_p, None)
        self.temperature = str_to_float(temperature, None)
        self.speed = str_to_float(speed, None)
    
    def __str__(self):
        return (f"refer_wav_path:{self.refer_wav_path}, "
                f"prompt_text:{self.prompt_text}, "
                f"prompt_language:{self.prompt_language}, "
                f"cut_punc:{self.cut_punc}, "
                f"top_k:{self.top_k}, "
                f"top_p:{self.top_p}, "
                f"temperature:{self.temperature}, "
                f"speed:{self.speed}")


class InferenceParamsManager:
    def __init__(self):
        self.default_params = InferenceParams()

    def set_default_params(self, default_params: InferenceParams):
        if default_params.refer_wav_path is not None:
            self.default_params.refer_wav_path = default_params.refer_wav_path
        if default_params.prompt_text is not None:
            self.default_params.prompt_text = default_params.prompt_text
        if default_params.prompt_language is not None:
            self.default_params.prompt_language = default_params.prompt_language
        if default_params.cut_punc is not None:
            self.default_params.cut_punc = default_params.cut_punc
        if default_params.top_k is not None:
            self.default_params.top_k = default_params.top_k
        if default_params.top_p is not None:
            self.default_params.top_p = default_params.top_p
        if default_params.temperature is not None:
            self.default_params.temperature = default_params.temperature
        if default_params.speed is not None:
            self.default_params.speed = default_params.speed

    def get_real_params(self, web_params: InferenceParams):
        return InferenceParams(
            refer_wav_path=get_params(web_params.refer_wav_path, self.default_params.refer_wav_path, None),
            prompt_text=get_params(web_params.prompt_text, self.default_params.prompt_text, None),
            prompt_language=get_params(web_params.prompt_language, self.default_params.prompt_language, None),
            cut_punc=get_params(web_params.cut_punc, self.default_params.cut_punc, None),
            top_k=get_params(web_params.top_k, self.default_params.top_k, 10),
            top_p=get_params(web_params.top_p, self.default_params.top_p, 1.0),
            temperature=get_params(web_params.temperature, self.default_params.temperature, 1.0),
            speed=get_params(web_params.speed, self.default_params.speed, 1.0)
        )


def get_params(web_params, exists_params, default_params):
    if web_params is not None:
        return web_params
    if exists_params is not None:
        return exists_params
    return default_params
