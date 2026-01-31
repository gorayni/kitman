import os
from pathlib import Path
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


class Builder(ABC):
    def __init__(self, path: Union[str, Path], transformations=None):
        self.path = Path(path)
        if transformations is None:
            self.transformations = []
        elif not isinstance(transformations, list):
            self.transformations = [transformations]
        else:
            self.transformations = transformations

    def apply_transformations(self, *substitutions):
        substitutions_ = []
        for s in substitutions:
            for t in self.transformations:
                s = t.apply(s)
            substitutions_.append(s)
        return tuple(substitutions_)

    def __getitem__(self, *substitutions):
        args = (
            substitutions[0] if isinstance(substitutions[0], tuple) else substitutions
        )
        return self.__call__(*args)


class BuildFilename(Builder):
    def __init__(self, path, filename_template, transformations=None):
        super().__init__(path, transformations)
        self.filename_template = filename_template

    def __call__(self, *substitutions):
        substitutions = self.apply_transformations(*substitutions)
        filename = self.filename_template.format(*substitutions)
        return self.path.joinpath(filename)

    @staticmethod
    def create(path, filename_template, transformations=None):
        if isinstance(filename_template, list):
            filename_template = os.path.join(*filename_template)

        if re.search(r".*(\{\:?.*\}).*", filename_template):
            return BuildFilename(path, filename_template, transformations)
        else:
            return path / filename_template


class HierarchicalFilenameBuilder(Builder):
    def __init__(
        self, path: Union[str, Path], filepath_templates: List, transformations=None
    ):
        super().__init__(path, transformations)
        
        self.remaining = [
            os.path.join(*t) if isinstance(t, list) else t for t in filepath_templates
        ]

        self.filepath_templates = []
        for i in range(len(filepath_templates)):
            self.filepath_templates.append(os.path.join(*self.remaining[: i + 1]))

    def __call__(self, *substitutions):
        num_args = len(substitutions)
        if num_args == 0 or num_args > len(self.filepath_templates):
            raise ValueError(
                f"Expected 1 to {len(self.filepath_templates)} arguments, got {num_args}"
            )
        substitutions = self.apply_transformations(*substitutions)

        result_path = self.path / self.filepath_templates[num_args - 1].format(
            *substitutions
        )

        if num_args < len(self.filepath_templates):
            return HierarchicalFilenameBuilder(
                result_path, self.remaining[num_args:], self.transformations
            )
        return result_path


class DirPathsBuilder:
    def __init__(
        self,
        base_path: Union[str, os.PathLike, Path],
        file_templates,
        transformations=None,
    ):
        self.base_path = Path(base_path)
        self.file_templates = file_templates
        self.transformations = transformations

        for attribute, filename_template in self.file_templates.items():
            contains_list = any(isinstance(i, list) for i in filename_template)
            if contains_list:
                builder = HierarchicalFilenameBuilder(
                    self.base_path, filename_template, transformations
                )
            else:
                builder = BuildFilename.create(
                    self.base_path, filename_template, transformations
                )
            setattr(self, attribute, builder)


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
