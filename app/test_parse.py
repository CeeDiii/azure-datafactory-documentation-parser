from .parse import parse_global_parameters, parse_udf_functions_with_comments
from unittest import TestCase


def test_parse_global_parameters():
    sample_file_content = b"ewogICAgICAgICAgICAiU3VwcG9ydGVkTGFuZ3VhZ2VzIjogewogICAgICAgICAgICAgICAgInR5cGUiOiAiYXJyYXkiLAogICAgICAgICAgICAgICAgInZhbHVlIjogWyJlbiIsICJkZSIsICJmciJdCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJNYXhNb250aHNIaXN0b3JpY2FsIjogewogICAgICAgICAgICAgICAgInR5cGUiOiAiaW50IiwKICAgICAgICAgICAgICAgICJ2YWx1ZSI6IDI0CiAgICAgICAgICAgIH0KICAgICAgICB9"
    expected = {
        "SupportedLanguages": {"type": "array", "value": ["en", "de", "fr"]},
        "MaxMonthsHistorical": {"type": "int", "value": 24},
    }
    actual = parse_global_parameters(sample_file_content)
    TestCase().assertDictEqual(expected, actual.model_dump())


def test_parse_udf_functions_with_single_full_documentation():
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
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

    TestCase().assertListEqual(expected, actual)


def test_parse_udf_functions_with_single_tag():
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
                            "CustomDivide(double, double) as double = /*",
                            ":Params:\r",
                            "i1=double, i2=double (cannot be 0)\r",
                            ":Params:\r",
                            "*/\r",
                            "\r",
                            "divide(i1, i2)",
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
                    "definition": "divide(i1, i2)",
                    "documentation": "",
                    "params": "i1=double, i2=double (cannot be 0)",
                    "examples": "",
                }
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    TestCase().assertListEqual(expected, actual)


def test_parse_udf_functions_with_two_tags():
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
                            "CustomDivide(double, double) as double = /*",
                            ":Documentation:\r",
                            "Divide two values and return the quotient.\r",
                            ":Documentation:\r",
                            "\r",
                            ":Params:\r",
                            "i1=double, i2=double (cannot be 0)\r",
                            ":Params:\r",
                            "\r",
                            "*/\r",
                            "\r",
                            "divide(i1, i2)",
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
                    "definition": "divide(i1, i2)",
                    "documentation": "Divide two values and return the quotient.",
                    "params": "i1=double, i2=double (cannot be 0)",
                    "examples": "",
                }
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    TestCase().assertListEqual(expected, actual)


def test_parse_udf_functions_with_no_tags():
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
                            "CustomDivide(double, double) as double = divide(i1, i2)"
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
                    "definition": "divide(i1, i2)",
                    "documentation": "",
                    "params": "",
                    "examples": "",
                }
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    TestCase().assertListEqual(expected, actual)


def test_parse_udf_functions_with_multiple_full_documentation():
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
                            "CustomDivide(double, double) as double = /*",
                            ":Documentation:\r",
                            "Divide two values and return the quotient.\r",
                            ":Documentation:\r",
                            "\r",
                            ":Params:\r",
                            "i1=double, i2=double (cannot be 0)\r",
                            ":Params:\r",
                            "\r",
                            ":Example:\r",
                            "CustomDivide(4.2, 2.1) -> 2.0\r",
                            ":Example:\r",
                            "*/\r",
                            "\r",
                            "divide(i1, i2),",
                            "CustomAdd(double, double) as double = /*",
                            ":Documentation:\r",
                            "Add two values and return the sum.\r",
                            ":Documentation:\r",
                            "\r",
                            ":Params:\r",
                            "i1=double, i2=double\r",
                            ":Params:\r",
                            "\r",
                            ":Example:\r",
                            "CustomAdd(4.2, 2.1) -> 6.3\r",
                            ":Example:\r",
                            "*/\r",
                            "\r",
                            "add(i1, i2),",
                            "CustomSubtract(double, double) as double = /*",
                            ":Documentation:\r",
                            "Subtract the second value from the first and return the subtractor.\r",
                            ":Documentation:\r",
                            "\r",
                            ":Params:\r",
                            "i1=double, i2=double\r",
                            ":Params:\r",
                            "\r",
                            ":Example:\r",
                            "CustomSubtract(4.2, 2.1) -> 2.1\r",
                            ":Example:\r",
                            "*/\r",
                            "\r",
                            "subtract(i1, i2)",
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
                    "definition": "divide(i1, i2)",
                    "documentation": "Divide two values and return the quotient.",
                    "params": "i1=double, i2=double (cannot be 0)",
                    "examples": "CustomDivide(4.2, 2.1) -> 2.0",
                },
                {
                    "name": "CustomAdd",
                    "declaration": "CustomAdd(double, double) as double",
                    "definition": "add(i1, i2)",
                    "documentation": "Add two values and return the sum.",
                    "params": "i1=double, i2=double",
                    "examples": "CustomAdd(4.2, 2.1) -> 6.3",
                },
                {
                    "name": "CustomSubtract",
                    "declaration": "CustomSubtract(double, double) as double",
                    "definition": "subtract(i1, i2)",
                    "documentation": "Subtract the second value from the first and return the subtractor.",
                    "params": "i1=double, i2=double",
                    "examples": "CustomSubtract(4.2, 2.1) -> 2.1",
                },
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    TestCase().assertListEqual(expected, actual)


def test_parse_udf_functions_with_multiple_mixed_documentation():
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
                            "CustomDivide(double, double) as double = /*",
                            ":Documentation:\r",
                            "Divide two values and return the quotient.\r",
                            ":Documentation:\r",
                            "\r",
                            ":Params:\r",
                            "i1=double, i2=double (cannot be 0)\r",
                            ":Params:\r",
                            "\r",
                            ":Example:\r",
                            "CustomDivide(4.2, 2.1) -> 2.0\r",
                            ":Example:\r",
                            "*/\r",
                            "\r",
                            "divide(i1, i2),",
                            "CustomAdd(double, double) as double = add(i1, i2),",
                            "CustomSubtract(double, double) as double = /*",
                            ":Documentation:\r",
                            "Subtract the second value from the first and return the subtractor.\r",
                            ":Documentation:\r",
                            "*/\r",
                            "\r",
                            "subtract(i1, i2)",
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
                    "definition": "divide(i1, i2)",
                    "documentation": "Divide two values and return the quotient.",
                    "params": "i1=double, i2=double (cannot be 0)",
                    "examples": "CustomDivide(4.2, 2.1) -> 2.0",
                },
                {
                    "name": "CustomAdd",
                    "declaration": "CustomAdd(double, double) as double",
                    "definition": "add(i1, i2)",
                    "documentation": "",
                    "params": "",
                    "examples": "",
                },
                {
                    "name": "CustomSubtract",
                    "declaration": "CustomSubtract(double, double) as double",
                    "definition": "subtract(i1, i2)",
                    "documentation": "Subtract the second value from the first and return the subtractor.",
                    "params": "",
                    "examples": "",
                },
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    TestCase().assertListEqual(expected, actual)


def test_parse_udf_functions_with_multiple_no_tags():
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
                            "CustomDivide(double, double) as double = divide(i1, i2),",
                            "CustomAdd(double, double) as double = add(i1, i2),",
                            "CustomSubtract(double, double) as double = subtract(i1, i2)",
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
            "description": "Some Description",
            "functions": [
                {
                    "name": "CustomDivide",
                    "declaration": "CustomDivide(double, double) as double",
                    "definition": "divide(i1, i2)",
                    "documentation": "",
                    "params": "",
                    "examples": "",
                },
                {
                    "name": "CustomAdd",
                    "declaration": "CustomAdd(double, double) as double",
                    "definition": "add(i1, i2)",
                    "documentation": "",
                    "params": "",
                    "examples": "",
                },
                {
                    "name": "CustomSubtract",
                    "declaration": "CustomSubtract(double, double) as double",
                    "definition": "subtract(i1, i2)",
                    "documentation": "",
                    "params": "",
                    "examples": "",
                },
            ],
        }
    ]

    actual = [
        lib.model_dump()
        for lib in parse_udf_functions_with_comments(sample_file_content)
    ]

    TestCase().assertListEqual(expected, actual)
