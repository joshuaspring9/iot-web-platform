#!/bin/bash

FILE="./.djangosql"

if [ ! -f $FILE ]
then
    read -p "Enter your mysql user(root is default): " user
    [ -z "$user" ] && user="root"
    read -p "Enter your mysql password: " pass

    echo "[django]" >> $FILE
    echo "user=${user}" >> $FILE
    echo "password=${pass}" >> $FILE

    chmod 0400 $FILE

    /usr/bin/expect <<-EOF
        spawn mysql_config_editor set --login-path=django --host=localhost --user=$user --password
        expect "Enter password: "
        send "${pass}\r"
        expect eof
	EOF
    echo Setup Complete
fi

echo "resetting database"
mysql --login-path=django <<EOF
DROP DATABASE IF EXISTS django_dashboard;
CREATE DATABASE django_dashboard;
EOF
python3 manage.py migrate



