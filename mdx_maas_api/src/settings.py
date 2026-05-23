from dotenv import dotenv_values

config = dotenv_values(".env")
MAAS_API_BASE_URL = config.get("MAAS_API_BASE_URL")
MAAS_API_KEY = config.get("MAAS_API_KEY")
