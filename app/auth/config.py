import os
import toml

config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
CONFIG_PATH = os.path.join(config_dir, 'project.toml')
config = toml.load(CONFIG_PATH)

SECRET_KEY = config["auth"]["secret_key"]
ALGORITHM = config["auth"]["algorithm"]
ACCESS_TOKEN_MINUTES = config["auth"]["access_token_expire_minutes"]
