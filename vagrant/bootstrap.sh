#!/bin/bash
SERVER_USERNAME="cjung-mo"
SERVER_USER_PASSWORD="cjung-mo"

function create_user() {
	# check if the new user already exists.
	if id -u $SERVER_USERNAME > /dev/null 2>&1; then
	    echo "User $SERVER_USERNAME already exists."
	else
	    sudo useradd -m -s /bin/bash -p $(echo $SERVER_USERNAME| openssl passwd -1 -stdin) $SERVER_USER_PASSWORD
	    sudo usermod -aG sudo $SERVER_USERNAME
	    echo "User $SERVER_USERNAME created."
	fi
}

# configure PostgreSQL 
function configure_postgres() {
    echo "Configuring PostgreSQL..."
    # we execute SQL commands as system user 'postgres'
    # 'psql -c' allows to execute a command without entering interpretor
    sudo -u postgres psql -c "CREATE DATABASE formationdjango;"
    sudo -u postgres psql -c "CREATE USER djangouser WITH PASSWORD 'secret';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE formationdjango TO djangouser;"
    echo "PostgreSQL configured."
}

function installation() {
	sudo apt update
	sudo apt install -y build-essential libpq-dev postgresql postgresql-contrib
	sudo apt install -y python3 python3-pip python3-dev python3.10-venv
}

create_user
installation
configure_postgres
