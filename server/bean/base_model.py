class BaseModel:
    @staticmethod
    def snake_to_camel(snake_str):
        """Converts a snake_case string to camelCase."""
        components = snake_str.split('_')
        # 如果字符串只有一个部分，则保持不变；否则首字母大写并拼接
        return components[0] + ''.join(x.title() for x in components[1:])

    def to_camel_case_dict(self):
        """Converts the instance attributes to a dictionary with camelCase keys."""
        return {self.snake_to_camel(k): to_camel_case_dict_if_is_base_model(v) for k, v in self.__dict__.items()}


def to_camel_case_dict_if_is_base_model(item):
    if isinstance(item, BaseModel) and hasattr(item, 'to_camel_case_dict'):
        return item.to_camel_case_dict()
    if isinstance(item, list):
        return convert_list_to_camel_case_dicts(item)
    else:
        return item


def convert_list_to_camel_case_dicts(list):
    result = []
    for item in list:
        if isinstance(item, BaseModel):
            result.append(item.to_camel_case_dict())
        else:
            result.append(item)
    return result
