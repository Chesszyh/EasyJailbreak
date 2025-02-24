"""
Constraint Base: Used to filter out prompts that do not conform to certain rules after mutation
定义一个抽象基类，用于在数据集变异后应用约束。
================================================================================================
This module defines an abstract base class for constraints applied to jailbreak datasets. These constraints
are used to refine the results of mutations by removing or altering prompts that do not meet specific criteria,
ensuring the dataset remains consistent with desired standards and rules.
"""

from abc import ABC, abstractmethod
from ..datasets import Instance, JailbreakDataset

__all__ = ["ConstraintBase"] # 模块的公开接口，import *时只会导入ConstraintBase

class ConstraintBase(ABC):
    """
    An abstract base class for defining constraints on instances in a JailbreakDataset.
    These constraints are applied after mutation to filter out or modify instances that
    do not meet certain predefined criteria.
    """
    @abstractmethod # 抽象方法装饰器，子类必须实现该方法
    def __call__(self, jailbreak_dataset, *args, **kwargs) -> JailbreakDataset:
        """
        Applies the constraint to a given jailbreak dataset, generating a new dataset of instances
        that meet the constraint criteria. This method provides basic logic for processing each instance
        in the dataset. It should be overridden for specific constraint implementations.

        :param ~JailbreakDataset jailbreak_dataset: The dataset to which the constraint will be applied.
        :return ~JailbreakDataset: A new dataset containing instances that meet the constraint criteria.
        """
        raise NotImplementedError