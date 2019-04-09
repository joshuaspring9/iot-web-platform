#!/bin/bash

FILE="./.djangosql"

while true
do
    read -p "Do you want to rerun the setup? [Y/n] " yn
    case $yn in
        [yY]* ) echo Resetting
                [ -f FILE ] && chmod 0700 $FILE
                mysql_config_editor remove --login-path=django
                break
                ;;
        * ) echo Abort.
            exit 0
            ;;
    esac
done

> $FILE

read -p "Enter your mysql user(root is default): " user
[ -z "$user" ] && user="root"
read -p "Enter your mysql password: " pass

echo "[django]" >> $FILE
echo "user=${user}" >> $FILE
echo "password=${pass}" >> $FILE

chmod 0400 $FILE

/usr/bin/expect <<EOF
    spawn mysql_config_editor set --login-path=django --host=localhost --user=$user --password
    expect "Enter password: "
    send "${pass}\r"
    expect EOF
EOF
echo Setup Complete
