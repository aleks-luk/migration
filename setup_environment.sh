export MYSQL_PASSWORD="MySqlPasswordHere"
export MYSQL_ROOT_PASSWORD="MySqlRootPasswordHere"
export POSTGRES_PASSWORD="PostgresPasswordHere"

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

docker-compose pull

docker-compose up -d