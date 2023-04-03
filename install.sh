#!/bin/bash
commande=false
if command -v python3
then
    commande="python3"
elif command -v python
then
    commande="python"
fi

if [ $commande != false ]
then
    $commande --version
else
    echo "python3 nécessaire"
    exit
fi

pip=false
if command -v pip3
then
    pip="pip3"
elif command -v pip
then
    pip="pip"
fi

if [ $pip != false ]
then
    $pip --version
else
    echo "pip nécessaire"
    exit
fi

$pip install -r requirements.txt
echo "Si tout s'est bien installé, complétez le fichier config.ini puis lancez la commande '$commande launch.py'"