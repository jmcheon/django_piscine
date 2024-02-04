#!/bin/sh

URL=$1


#if [[ $URL != https://* ]]; then
	#URL="https://"$URL
#fi

case "$URL" in
    https://*) ;;
    *) URL="https://$URL" ;;
esac

curl -s -D - $URL | grep "location" | cut -d' ' -f2
