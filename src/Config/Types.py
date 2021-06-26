# App Config
SECRET_KEY 	 = "ae0d1f37049f90405e5533a1b78168d16db1b1e258c8a0bb85fce05ad74c16ca45e93b66f9916a1c1948c6601fd8986398b659f2629a0bc8c6c6ba879cb52c31"

# Database Config
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{dbUserName}:{dbPassword}@{dbHost}/{dbName}".format(
	dbUserName="julo_mini_wallet_services",
	dbPassword="$2y$12$SdVbjfnP5uPieHj5/awRJ.DpXsJkRvac0As//YDu0wR2DRpBaD9ra",
	dbHost="julo_postgres_mini_wallet_servcies",
	dbName="julo_mini_wallet_services"
)