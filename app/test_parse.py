from .parse import parse_global_parameters, parse_udf_functions_with_comments
from unittest import TestCase


def test_parse_global_parameters_expect_pass():
    sample_file_content = b"ewogICAgICAgICAgICAiU3VwcG9ydGVkTGFuZ3VhZ2VzIjogewogICAgICAgICAgICAgICAgInR5cGUiOiAiYXJyYXkiLAogICAgICAgICAgICAgICAgInZhbHVlIjogWyJlbiIsICJkZSIsICJmciJdCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJNYXhNb250aHNIaXN0b3JpY2FsIjogewogICAgICAgICAgICAgICAgInR5cGUiOiAiaW50IiwKICAgICAgICAgICAgICAgICJ2YWx1ZSI6IDI0CiAgICAgICAgICAgIH0KICAgICAgICB9"
    expected = {
        "SupportedLanguages": {"type": "array", "value": ["en", "de", "fr"]},
        "MaxMonthsHistorical": {"type": "int", "value": 24},
    }
    actual = parse_global_parameters(sample_file_content)
    TestCase().assertDictEqual(expected, actual.model_dump())


def test_parse_udf_functions_with_comments_expect_pass():
    sample_file_content = {
        "resources": [
            {
                "name": "[concat(parameters('factoryName'), '/SomeLibrary')]",
                "type": "Microsoft.DataFactory/factories/dataflows",
                "apiVersion": "2018-06-01",
                "description": "Some Description",
                "properties": {
                    "type": "UDFLibrary",
                    "typeProperties": {
                        "sources": [],
                        "sinks": [],
                        "transformations": [],
                        "scriptLines": [
                            "CustomDivide(double, double) as double = /*"
                            ":Documentation:\r"
                            "Divide two values and return the quotient.\r"
                            ":Documentation:\r"
                            "\r"
                            ":Params:\r"
                            "i1=double, i2=double (cannot be 0)\r"
                            ":Params:\r"
                            "\r"
                            ":Example:\r"
                            "CustomDivide(4.2, 2.1) -> 2.0\r"
                            ":Example:\r"
                            "*/\r"
                            "\r"
                            "divide(i1, i2)"
                        ],
                    },
                },
                "dependsOn": [],
            }
        ]
    }

    expected = [
        {
            "name": "SomeLibrary",
            "description": "",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double ",
                    "definition": "divide(i1, i2)",
                    "documentation": "Divide two values and return the quotient.",
                    "params": "i1=double, i2=double (cannot be 0)",
                    "examples": "CustomDivide(4.2, 2.1) -> 2.0",
                }
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    print(expected)
    print(actual)
    TestCase().assertListEqual(expected, actual)
