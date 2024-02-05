#!/bin/bash
set -e
PUSH_LOCAL_DATA=1
INSTALL_DEPS=1
DEPLOY_DIR=/srv/baby-tracker

usage()
{
    echo "usage: ./deploy.sh [-h|--help] [--deps] [--push-data]"
}

deploy()
{
    ssh $USER@$REMOTE_HOST "mkdir -p ${DEPLOY_DIR}"
    scp requirements.txt $USER@$REMOTE_HOST:${DEPLOY_DIR}/
    scp main.sh $USER@$REMOTE_HOST:${DEPLOY_DIR}/
    rsync -rav -e ssh  --exclude='__pycache__' ./baby_tracker $USER@$REMOTE_HOST:${DEPLOY_DIR}/
    scp create-venv.sh $USER@$REMOTE_HOST:${DEPLOY_DIR}/

    if [ $INSTALL_DEPS == 0 ]
    then
        ssh $USER@$REMOTE_HOST "apt-get update && apt-get install python3-venv supervisor sqlite3 -y"
        ssh $USER@$REMOTE_HOST "cd $DEPLOY_DIR && ./create-venv.sh"
    fi

    if [ $PUSH_LOCAL_DATA == 0 ]
    then
        rsync -rav -e ssh  --exclude='__pycache__' ./data $USER@$REMOTE_HOST:${DEPLOY_DIR}/
        ssh $USER@$REMOTE_HOST "cd $DEPLOY_DIR && ./data/import.sh"
    fi
    scp supervisor.conf $USER@$REMOTE_HOST:/etc/supervisor/conf.d/baby-tracker.conf
    ssh $USER@$REMOTE_HOST "supervisorctl reread; supervisorctl update; supervisorctl restart baby_tracker"
}



while [ "$1" != "" ]; do
    case $1 in
        --deps)
            INSTALL_DEPS=0;; 

        --push-data) 
            PUSH_LOCAL_DATA=0;;

        -h | --help) 
            usage;exit 0;;

        *)
            usage;exit 1;;
    esac
    shift
done
deploy