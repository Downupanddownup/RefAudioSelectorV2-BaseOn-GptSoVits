from server.bean.base_model import BaseModel, convert_list_to_camel_case_dicts


def convert_dict_to_camel_case_dicts(dict_obj: dict):

    result = {}
    for key, value in dict_obj.items():
        if isinstance(value, BaseModel):
            result[key] = value.to_camel_case_dict()
        elif isinstance(value, list):
            result[key] = convert_list_to_camel_case_dicts(value)
        else:
            result[key] = value
    return result


class ResponseResult:
    def __init__(self, code=0, msg="success", count=0, data=None):
        self.code = code
        self.msg = msg
        self.count = count
        self.data = None
        if isinstance(data, list):
            self.data = convert_list_to_camel_case_dicts(data if data is not None else [])
        else:
            if data is not None:
                if isinstance(data, BaseModel):
                    self.data = data.to_camel_case_dict()
                elif isinstance(data, dict):
                    self.data = convert_dict_to_camel_case_dicts(data)
                else:
                    self.data = data

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "count": self.count,
            "data": self.data
        }

    def __str__(self):
        return f"ResponseResult(code={self.code}, msg='{self.msg}', count={self.count}, data={self.data})"
