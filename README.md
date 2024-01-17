<p align="center">
    <h1 align="center">AZURE-DATAFACTORY-DOCUMENTATION-PARSER</h1>
</p>
<p align="center">
    <em>A self-hosted solution to share and access documentation of global parameters and user defined functions in Azure Data Factory.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/CeeDiii/azure-datafactory-documentation-parser?style=flat-square&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/CeeDiii/azure-datafactory-documentation-parser?style=flat-square&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/CeeDiii/azure-datafactory-documentation-parser?style=flat-square&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/CeeDiii/azure-datafactory-documentation-parser?style=flat-square&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat-square&logo=FastAPI&logoColor=white" alt="FastAPI">
</p>
<hr>

## 🔗 Quick Links

> -   [📍 Overview](#-overview)
> -   [👨‍🏫 How to](#👨‍🏫-how-to)
> -   [🚀 Getting Started](#-getting-started)
>     -   [⚙️ Installation](#️-installation)
>     -   [📝 Prerequisites](#-prerequisites)
>     -   [🤖 Running azure-datafactory-documentation-parser](#-running-azure-datafactory-documentation-parser)
>     -   [🧪 Tests](#-tests)
> -   [🤝 Contributing](#-contributing)
> -   [📄 License](#-license)
> -   [👏 Acknowledgments](#-acknowledgments)

---

## 👨‍🏫 How to

This tool reads your Azure Data Factory's Github repository and parses the global parameters from the `YOUR_FACTORY_NAME_GlobalParameters.json` and the user defined functions from the `ARMTemplateForFactory.json`. By in-lining with simple, custom markup you can document your functions and highly increase the comprehensibility of your UDF for collaborators.

There are two available endpoints `/docs/datafactory/global-parameters` and `/docs/datafactory/user-defined-functions`.

### `/docs/datafactory/global-parameters`

Return the global parameters as is.

E.g.

```json
{
    "SupportedLanguages": {
        "type": "array",
        "value": ["en", "de", "fr"]
    },
    "MaxMonthsHistorical": {
        "type": "int",
        "value": 24
    }
}
```

### `/docs/datafactory/user-defined-functions`

The following markup is supported and the content between and open and a closing tag will be parsed:

<table>
<thead>
    <tr>
        <th>Markup</th>
        <th>Usage</th>
    <tr>
</thead>
<tbody>
    <tr>
        <td>:Documentation:</td>
        <td>Add any descriptive comments as text.</td>
    </tr>
    <tr>
        <td>:Params:</td>
        <td>Declare the params and their types.</td>
    </tr>
    <tr>
        <td>:Example:</td>
        <td>Add an example on how to use the function.</td>
    </tr>
</tbody>
</table>

Here is an example of how this could look:

Azure Data Factory Data Flow Function body:

```sh
/*
:Documentation:
Divide two values and return the quotient.
:Documentation:

:Params:
i1=double, i2=double (cannot be 0)
:Params:

:Example:
CustomDivide(4, 2) -> 2
:Example:
*/

divide(i1, i2)
```

Given this input the endpoint `/docs/datafactory/user-defined-functions` returns:

```json
[
    {
        "name": "SomeLibrary",
        "description": "Some Description",
        "functions": [
            {
                "name": "CustomDivide",
                "declaration": "CustomDivide(double, double) as double",
                "definition": "divide(i1, i2)",
                "documentation": "Divide two values and return the quotient.",
                "params": "i1=double, i2=double (cannot be null)",
                "examples": "CustomDivide(4.2, 2.1) -> 2.0"
            }
        ]
    }
]
```

---

## 📍 Overview

Collaboration in Azure Data Factory is not a simple task. This self-hosted solution aims to improve readability and comprehensibility of global parameters and user-defined functions in Azure Data Factory. By adhering to simple guide lines we can parse code-like documentation from functions and return them as json to render them in the documentation tool of your team's choice.

---

## 🚀 Getting Started

**_Requirements_**

Ensure you have the following dependencies installed on your system:

-   **Python**: `version >3.10.*`

### 📝 Prerequisites

Make sure your Data Factory is connected to Github. Other source control systems are currently not supported. [Check this tutorial to setup Github source control for your Factory](https://learn.microsoft.com/en-us/azure/data-factory/source-control).

### ⚙️ Installation

1. Clone the azure-datafactory-documentation-parser repository:

```sh
git clone https://github.com/CeeDiii/azure-datafactory-documentation-parser
```

2. Change to the project directory:

```sh
cd azure-datafactory-documentation-parser
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

### 🤖 Running azure-datafactory-documentation-parser

Create a `.env` file with the following content:

```sh
GITHUB_ADF_TOKEN="YOUR_GITHUB_API_TOKEN"
ORGANIZATION_NAME="YOUR_GITHUB_ORGANIZATION_OR_USER_NAME"
FACTORY_NAME="YOUR_AZURE_DATA_FACTORY_NAME"
```

Use the following command to start the fastapi development server:

```sh
uvicorn app.main:app --reload
```

### 🧪 Tests

To execute tests, run:

```sh
pytest
```

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

-   **[Submit Pull Requests](https://github/CeeDiii/azure-datafactory-documentation-parser/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
-   **[Join the Discussions](https://github/CeeDiii/azure-datafactory-documentation-parser/discussions)**: Share your insights, provide feedback, or ask questions.
-   **[Report Issues](https://github/CeeDiii/azure-datafactory-documentation-parser/issues)**: Submit bugs found or log feature requests for Azure-datafactory-documentation-parser.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
    ```sh
    git clone https://github.com/CeeDiii/azure-datafactory-documentation-parser
    ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
    ```sh
    git checkout -b new-feature-x
    ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
    ```sh
    git commit -m 'Implemented new feature x.'
    ```
6. **Push to GitHub**: Push the changes to your forked repository.
    ```sh
    git push origin new-feature-x
    ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

## 📄 License

[MIT](https://github.com/eli64s/readme-ai/blob/main/LICENSE)

---

## 👏 Acknowledgments

-   [readme-ai](https://github.com/eli64s/readme-ai/tree/main)

[**Return**](#-quick-links)

---
