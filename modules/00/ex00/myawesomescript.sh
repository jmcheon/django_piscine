#!/bin/bash

URL="https://"$1

curl -s -D - $URL | grep "location" | cut -d' ' -f2
