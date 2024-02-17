#!/bin/bash
trap 'echo "Script interrumpido por el usuario"; exit' SIGINT
while true; do
    echo "Haciendo ping a google.cl..."
    ping -c 2 google.cl
    echo "Listando archivos en el directorio actual..."
    ls -la
    ls --color=auto
    pwd
    clear
    echo "Hacking class, Profesor!!!"
    echo "=-=-=-=-=-=-=-=-=-=-=-=-=-"
    echo "detect in progress ..."
    sleep 5
done
 
