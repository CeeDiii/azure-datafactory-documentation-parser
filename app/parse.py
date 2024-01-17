import base64
from typing import Any, List, Dict

from .models import GlobalParameters, UserDefinedFunctionLibrary


def _get_content_for_tag(search_text: str, tag: str) -> str:
    """
    Extracts content between the given tag in the search_text.

    Parameters:
    - search_text (str): The text to search within.
    - tag (str): The tag to extract content for.

    Returns:
    str: The content between the tags.
    """
    start_index = search_text.find(tag) + len(tag)
    end_index = search_text.rfind(tag)
    if start_index >= 0 and end_index > start_index:
        return search_text[start_index:end_index]
    else:
        return ""


def _parse_isolated_function_strings(function_strings: List[str]) -> List[str]:
    """
    Parses isolated function strings from a list of function strings.

    Parameters:
    - function_strings (List[str]): List of function strings.

    Returns:
    List[str]: List of isolated function strings.
    """
    single_function_string = ""
    isolated_function_strings = []
    for line in function_strings:
        if "/*" in line and single_function_string != "":
            isolated_function_strings.append(single_function_string)
            single_function_string = ""
        line += "\n"
        single_function_string += line
    isolated_function_strings.append(single_function_string)  # append final string
    return isolated_function_strings


def _parse_function_content(single_function_string: str) -> Dict[str, str]:
    """
    Parses function content from a single function string.

    Parameters:
    - single_function_string (str): The function string to parse.

    Returns:
    Dict[str, str]: Dictionary containing function information.
    """
    documentation_tags = ":Documentation:"
    params_tag = ":Params:"
    example_tags = ":Example:"

    comment_start_index = single_function_string.find("= /*")
    comment_end_index = single_function_string.find("*/") + len("*/")

    declaration_content = single_function_string[:comment_start_index]
    function_name = declaration_content.split("(")[0].strip()
    definition_content = single_function_string[comment_end_index:-2].strip()

    documentation_content = _get_content_for_tag(
        single_function_string, documentation_tags
    ).strip()
    params_content = _get_content_for_tag(single_function_string, params_tag).strip()
    example_content = _get_content_for_tag(single_function_string, example_tags).strip()

    return {
        "name": function_name,
        "declaration": declaration_content,
        "definition": definition_content,
        "documentation": documentation_content,
        "params": params_content,
        "examples": example_content,
    }


def parse_global_parameters(file_content: str) -> GlobalParameters:
    """
    Parses Global Parameters from 'YOUR_DATA_FACTORY_GlobalParameters.json'.

    Parameters
    ----------
    - file_content (str): String content of the json file.

    Returns
    -------
    GlobalParameters
    """
    decoded_bytes = base64.b64decode(file_content)
    decoded_str = str(decoded_bytes, "utf-8")
    global_parameters = GlobalParameters.model_validate_json(decoded_str)
    return global_parameters


def parse_udf_functions_with_comments(
    file_content: Dict[str, Any]
) -> List[UserDefinedFunctionLibrary]:
    """
    Parses UDF functions with comments from an ARM template.

    Parameters:
    - file_content (dict): ARM template content.

    Returns:
    -------
    List[UserDefinedFunctionLibrary]
    """
    resources = file_content.get("resources", [])
    udf_library = [
        res
        for res in resources
        if res.get("properties", {}).get("type") == "UDFLibrary"
    ]

    functions_strings = [
        lib.get("properties", {}).get("typeProperties", {}).get("scriptLines", [])
        for lib in udf_library
    ]
    function_strings_by_library = [
        _parse_isolated_function_strings(strings) for strings in functions_strings
    ]
    functions = [
        [
            _parse_function_content(isolated_function_string)
            for isolated_function_string in isolated_function_strings
        ]
        for isolated_function_strings in function_strings_by_library
    ]

    libraries = [
        {
            "name": lib.get("name", "")
            .replace("[concat(parameters('factoryName'), '/", "")
            .replace("')]", ""),
            "description": lib.get("properties", {}).get("description", ""),
            "functions": functions[index],
        }
        for index, lib in enumerate(udf_library)
    ]

    udf_libraries = list(
        map(
            lambda lib: UserDefinedFunctionLibrary(**lib),
            libraries,
        )
    )
    return udf_libraries
