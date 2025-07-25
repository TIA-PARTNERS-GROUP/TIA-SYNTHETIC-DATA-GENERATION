import toml

try:
    with open("./config.toml", "r") as f:
        config = toml.load(f)
except FileNotFoundError:
    raise FileNotFoundError("The 'config.toml' file was not found in the project directory.")

DB_CONNECTION_STRING = config.get("database_connection_string")
DATA_GENERATION_SIZE = config.get("data_generation_size", 50)

if not DB_CONNECTION_STRING:
    raise ValueError(
        "Database connection string not found. Please set it in 'config.toml' "
        "or as a DB_CONNECTION_STRING environment variable."
    )
