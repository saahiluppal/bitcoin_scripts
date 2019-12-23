#/usr/bin/bash

if which apt > /dev/null; then
	echo "apt package manager found"
	if which bitcoind >/dev/null; then
		echo "Already installed"
		exit 1
	fi
elif which dnf > /dev/null; then
	echo "dnf package manager found"
	if which bitcoind >/dev/null; then
		echo "Already installed"
		exit 1
	fi
fi
