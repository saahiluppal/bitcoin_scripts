#/usr/bin/bash

if which apt > /dev/null; then
	echo "apt package manager found"
	if which bitcoind >/dev/null; then
		echo "Already installed"
		exit 1
	fi
	echo "Installing Dependencies for Apt Package Manager"
	sudo apt install wget autoconf libtool libboost* libcurl4-openssl-dev libevent-dev libssl-dev
	bash libdb

	echo "Going Home"
	cd $HOME
	git clone https://github.com/bitcoin/bitcoin.git

	cd bitcoin
	git checkout v0.19.0.1
	git status

	echo "Running Autogen"
	./autogen.sh

	sleep 2

	echo "Configuring"
	./configure

	make
	sudo make install

	if which bitcoind>/dev/null; then
		echo "Successfully installed Bitcoin Node"
	else
		echo "Some Problem Might Occured inbetween Process;"
		echo "You can try again or may issue on https://github.com/saahiluppal/bitcoin_scripts/tree/master/install_Bitcoin_core_node"
	fi

elif which dnf > /dev/null; then
	echo "dnf package manager found"
	if which bitcoind >/dev/null; then
		echo "Already installed"
		exit 1
	fi
fi
