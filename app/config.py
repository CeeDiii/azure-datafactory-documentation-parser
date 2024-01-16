from pydantic_settings import BaseSettings, SettingsConfigDict


class GithubSettings(BaseSettings):
    base_url: str = "https://api.github.com/repos"
    repository_name: str = "azure-datafactory"
    branch_name: str = "adf_publish"
    organization_name: str
    factory_name: str
    github_adf_token: str

    model_config = SettingsConfigDict(env_file=".env")
