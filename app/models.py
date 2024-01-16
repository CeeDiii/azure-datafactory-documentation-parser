from typing import Any, Dict, List

from pydantic import BaseModel, RootModel


class GlobalParameter(BaseModel):
    type: str
    value: Any


class GlobalParameters(RootModel):
    root: Dict[str, GlobalParameter]


class UserDefinedFunction(BaseModel):
    name: str
    declaration: str
    definition: str
    documentation: str
    params: str
    examples: str


class UserDefinedFunctionLibrary(BaseModel):
    name: str
    description: str
    functions: List[UserDefinedFunction]
