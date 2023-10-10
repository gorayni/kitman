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

    def __getitem__(self, *substitutions):
        if isinstance(substitutions[0], tuple):
            substitutions = substitutions[0]
        return self.__call__(*substitutions)

    def __call__(self, *substitutions):
        substitutions_ = []
        for s in substitutions:
            if isinstance(s, (int, float, complex, np.integer, np.floating)):
                s += 1
            substitutions_.append(s)
        substitutions_ = tuple(substitutions_)
        filename = self.filename_template.format(*substitutions_)
        return self.path.joinpath(filename)

    @staticmethod
    def create(path, filename_template):
        if isinstance(filename_template, list):
            filename_template = os.path.join(*filename_template)

        if re.search(r'.*(\{\:?.*\}).*', filename_template):            
            return BuildFilename(path, filename_template)
        else:
            return path.joinpath(filename_template)


class DirPathsBuilder:
    def __init__(self, base_path, file_templates):
        self.base_path = base_path
        self.file_templates = file_templates

        for attribute, filename_template in self.file_templates.items():
            setattr(self, attribute, BuildFilename.create(self.base_path, filename_template))            


class Players:
    def __init__(self, idx: Union[NamedTuple, Type[IndicesClass]],
                 coords: Union[List[np.ndarray], np.ndarray] = None,
                 labels: Union[List[np.ndarray], np.ndarray] = None):        
        attributes = idx._fields if isinstance(idx, tuple) else vars(idx).keys()
        for attr in attributes:
            setattr(self, attr, getattr(idx, attr))
        self.coords = coords
        self.labels = labels

    def __len__(self):
        return len(self.coords)


class PlayerPatches(Players):
    def __init__(self, idx: Union[NamedTuple, Type[IndicesClass]],
                 patches: List[np.ndarray],
                 coords: Union[List[np.ndarray], np.ndarray] = None,
                 labels: Union[List[np.ndarray], np.ndarray] = None):
        super().__init__(idx, coords, labels)
        self.patches = patches

    def __len__(self):
        return len(self.patches)
