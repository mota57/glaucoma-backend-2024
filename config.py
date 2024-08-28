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
    STATIC_S3 = ConfigUtils.get_environment_variable('GLAUCOMA_STATIC_S3')
    STATIC_S3_IMAGE_DIRECTORY = f'https://{ConfigUtils.get_environment_variable("GLAUCOMA_STATIC_S3")}.s3.amazonaws.com/images/'
    DB_CONNECTION = "postgresql://postgres:Fanata57$@glaucoma-db.cfe04yc6glxz.us-east-1.rds.amazonaws.com/glaucoma-db"
