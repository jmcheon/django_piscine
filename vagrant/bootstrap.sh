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

function installation() {
	sudo apt update
	sudo apt install -y build-essential libpq-dev
	sudo apt install -y python3 python3-pip python3-dev python3.10-venv
}

create_user
installation
