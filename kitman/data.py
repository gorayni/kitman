import os
import re
from abc import ABC, abstractmethod
from typing import List, NamedTuple, Type, TypeVar, Union

import numpy as np


IndicesClass = TypeVar("IndicesClass")


class Transformation(ABC):
    @abstractmethod
    def apply(self, value):
        pass


class NonZeroBasedIndex(Transformation):
    def apply(self, value):
        if isinstance(value, (int, float, complex, np.integer, np.floating)):
            return value + 1
        return value


class BuildFilename:
    def __init__(self, path, filename_template, transformations=None):
        self.path = path
        self.filename_template = filename_template

        if transformations is None:
            self.transformations = []
        elif type(transformations) is not list:
            self.transformations = [transformations]
        else:
            self.transformations = transformations

    def __getitem__(self, *substitutions):
        if isinstance(substitutions[0], tuple):
            substitutions = substitutions[0]
        return self.__call__(*substitutions)

    def __call__(self, *substitutions):
        substitutions_ = []
        for s in substitutions:
            for t in self.transformations:
                s = t.apply(s)
            substitutions_.append(s)
        substitutions_ = tuple(substitutions_)
        filename = self.filename_template.format(*substitutions_)
        return self.path.joinpath(filename)

    @staticmethod
    def create(path, filename_template, transformations=None):
        if isinstance(filename_template, list):
            filename_template = os.path.join(*filename_template)

        if re.search(r".*(\{\:?.*\}).*", filename_template):
            return BuildFilename(path, filename_template, transformations)
        else:
            return path.joinpath(filename_template)


class DirPathsBuilder:
    def __init__(self, base_path, file_templates, transformations=None):
        self.base_path = base_path
        self.file_templates = file_templates
        self.transformations = transformations

        for attribute, filename_template in self.file_templates.items():
            setattr(
                self,
                attribute,
                BuildFilename.create(
                    self.base_path, filename_template, transformations
                ),
            )


class Players:
    def __init__(
        self,
        idx: Union[NamedTuple, Type[IndicesClass]],
        coords: Union[List[np.ndarray], np.ndarray] = None,
        labels: Union[List[np.ndarray], np.ndarray] = None,
    ):
        attributes = idx._fields if isinstance(idx, tuple) else vars(idx).keys()
        for attr in attributes:
            setattr(self, attr, getattr(idx, attr))
        self.coords = coords
        self.labels = labels

    def __len__(self):
        return len(self.coords)


class PlayerPatches(Players):
    def __init__(
        self,
        idx: Union[NamedTuple, Type[IndicesClass]],
        patches: List[np.ndarray],
        coords: Union[List[np.ndarray], np.ndarray] = None,
        labels: Union[List[np.ndarray], np.ndarray] = None,
    ):
        super().__init__(idx, coords, labels)
        self.patches = patches

    def __len__(self):
        return len(self.patches)
