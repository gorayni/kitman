import os
import re
from typing import List, \
    NamedTuple, \
    Type, \
    TypeVar, \
    Union

import numpy as np

IndicesClass = TypeVar('IndicesClass')


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


class PlayerPatches:
    def __init__(self, idx: Union[NamedTuple, Type[IndicesClass]],
                 patches: List[np.ndarray],
                 coords: Union[List[np.ndarray], np.ndarray] = None,
                 labels: Union[List[np.ndarray], np.ndarray] = None):
        attributes = idx._fields if isinstance(idx, tuple) else vars(idx).keys()
        for attr in attributes:
            setattr(self, attr, getattr(idx, attr))
        self.patches = patches
        self.coords = coords
        self.labels = labels

    def __len__(self):
        return len(self.patches)
