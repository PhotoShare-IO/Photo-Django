#!/bin/bash

while ! make migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done

make run-server