#!/bin/bash

if [ $# -gt 1 ]
then
    echo 'too many arguments'
    exit 0
fi

FILE="./iot-web-platform/local_settings.py"

if [ $# -eq 1 ]
then
    if [ "$1" = "s" ]
    then
        rFILE="./iot-web-platform/local_settings_dist.py"

        if [ -f $FILE ]
        then
            while true
            do
                read -p "Do you want to rerun the setup? [Y/n] " yn
                case $yn in
                    [yY]* ) echo Resetting
                            mysql_config_editor remove --login-path=django
                            break
                            ;;
                    * ) echo Abort.
                        exit 0
                        ;;
                esac
            done
        fi

        > $FILE

        read -p "Enter your mysql user(root is default): " user
        [ -z "$user" ] && user="root"

        while true
        do
        read -sp "Enter your mysql password: " pass
        [ -z "$pass" ] || break
        done

        sed "s/undefined/${user}/g; s/unique/${pass}/g" $rFILE > $FILE

        /usr/bin/expect << EOS
            spawn mysql_config_editor set --login-path=django --host=localhost --user=$user --password
            expect "Enter password: "
            send "${pass}\r"
            expect EOF
EOS
        echo Setup Complete
    else
        echo "unrecognized argument"
        exit 0
    fi

fi

if [ ! -f $FILE ]
then
    echo "please run setup.sh with argument s"
    exit 0
fi

echo "resetting database"
mysql --login-path=django <<EOF
DROP DATABASE IF EXISTS django_dashboard;
CREATE DATABASE django_dashboard;
EOF
python3 manage.py migrate