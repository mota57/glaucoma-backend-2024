import os

class MissingEnvironmentVariableError(Exception):
    """Raised when a required environment variable is missing."""
    pass

class ConfigUtils:

    @staticmethod
    def get_environment_variable(var_name):
        var_value = os.environ.get(var_name)
        if not var_value:
            raise MissingEnvironmentVariableError("Environment variable " + var_name +" is missing.")
        return var_value

class GlaucomaConfig:
    EB_GLAUCOMA_API_WEBSITE_STATIC_S3 = ConfigUtils.get_environment_variable('EB_GLAUCOMA_API_WEBSITE_STATIC_S3')

