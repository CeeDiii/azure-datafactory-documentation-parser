import base64
from functools import lru_cache
from typing import List

import requests
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from typing_extensions import Annotated


from .config import GithubSettings
from .models import GlobalParameters, UserDefinedFunctionLibrary
from .utils import parse_udf_functions_with_comments

app = FastAPI()


@lru_cache
def get_settings():
    """
    Create a singleton settings object on initialization of the app.

    Returns
    -------
    GithubSettings
        A configuration object.
    """
    return GithubSettings()


@app.get("/docs/datafactory/global-parameters")
def read_global_parameters(
    github_settings: Annotated[GithubSettings, Depends(get_settings)]
) -> GlobalParameters:
    """
    Read the global parameters from the Data Factory repository on Github and return it as json.

    Parameters
    ----------
    github_settings : Annotated[GithubSettings, Depends]
        The configuration object for this app.

    Returns
    -------
    GlobalParameters
        The global parameters stored in the Azure Data Factory.
    """
    headers = {
        "Authorization": f"Token {github_settings.github_adf_token}",
        "Accept": "application/vnd.github.json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        branch_suffix = (
            "?ref=" + github_settings.branch_name if github_settings.branch_name else ""
        )
        request_url = f"{github_settings.base_url}/{github_settings.organization_name}/{github_settings.repository_name}/contents/{github_settings.factory_name}/globalParameters/{github_settings.factory_name}_GlobalParameters.json{branch_suffix}"
        res = requests.get(request_url, headers=headers, timeout=30)

        if res.ok:
            data = res.json()
            decoded_bytes = base64.b64decode(data["content"])
            decoded_str = str(decoded_bytes, "utf-8")
            print(decoded_str)
            global_parameters = GlobalParameters.model_validate_json(decoded_str)
            return global_parameters
        else:
            return JSONResponse(
                status_code=res.status_code, content={"message": res.text}
            )

    except requests.HTTPError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": e.strerror},
        )


@app.get("/docs/datafactory/user-defined-functions")
def read_user_defined_functions(
    github_settings: Annotated[GithubSettings, Depends(get_settings)]
) -> List[UserDefinedFunctionLibrary]:
    """
    Read the user defined functions from the Data Factory on Github and return it as json.

    Parameters
    ----------
    github_settings : Annotated[GithubSettings, Depends]
        The configuration object for this app.

    Returns
    -------
    List[UserDefinedFunctionLibrary]
        The list of user defined function libraries stored in the Azure Data Factory.
    """
    headers = {
        "Authorization": f"Token {github_settings.github_adf_token}",
        "Accept": "application/vnd.github.raw",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        branch_suffix = (
            "?ref=" + github_settings.branch_name if github_settings.branch_name else ""
        )
        request_url = f"{github_settings.base_url}/{github_settings.organization_name}/{github_settings.repository_name}/contents/{github_settings.factory_name}/ARMTemplateForFactory.json{branch_suffix}"
        res = requests.get(request_url, headers=headers, timeout=30)

        if res.ok:
            data = res.json()
            parsed_function_libraries = parse_udf_functions_with_comments(data)
            udf_libraries = list(
                map(
                    lambda lib: UserDefinedFunctionLibrary(**lib),
                    parsed_function_libraries,
                )
            )
            return udf_libraries
        else:
            return JSONResponse(
                status_code=res.status_code, content={"message": res.text}
            )
    except requests.HTTPError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": e.strerror},
        )
