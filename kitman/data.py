import os
import re


class BuildFilename:
    def __init__(self, path, filename_template):
        self.path = path
        self.filename_template = filename_template

    def __getitem__(self, *_ids):
        if isinstance(_ids[0], tuple):
            _ids = _ids[0]
        return self.__call__(*_ids)

    def __call__(self, *_ids):
        _ids = tuple([_id + 1 for _id in _ids])
        filename = self.filename_template.format(*_ids)
        return self.path.joinpath(filename)


class DirPathsBuilder:
    def __init__(self, base_path, file_templates):
        self.base_path = base_path
        self.file_templates = file_templates

        for attribute, filename_template in self.file_templates.items():
            if isinstance(filename_template, list):
                filename_template = os.path.join(*filename_template)
            if re.search(r'.*(\{\:?.*\}).*', filename_template):
                setattr(self, attribute, BuildFilename(self.base_path, filename_template))
            else:
                setattr(self, attribute, self.base_path.joinpath(filename_template))
