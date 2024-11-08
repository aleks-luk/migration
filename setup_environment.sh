export MYSQL_PASSWORD="MySqlPasswordHere"
export MYSQL_ROOT_PASSWORD="MySqlRootPasswordHere"
export POSTGRES_PASSWORD="PostgresPasswordHere"

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setting up Docker containers..."
docker-compose up -d

echo "Generating sample data..."
python generate_data.py

echo "Running data migration..."
python migrate.py
