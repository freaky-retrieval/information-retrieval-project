#!/usr/bin/env bash
run_storage() {
    sudo docker run \
        -p 9000:9000 \
        -p 9001:9001 \
        --name minio \
        -v ~/minio/data:/data \
        -e "MINIO_ROOT_USER=minioadmin" \
        -e "MINIO_ROOT_PASSWORD=minioadmin" \
        quay.io/minio/minio server /data --console-address ":9001"
}

wait_for_minio_running() {
    echo "Wait for MinIO Starting..."
    while true; do
        res=$(sudo docker ps | grep minio | grep Up | wc -l)
        if [ $res -eq 1 ]; then
            echo "Start successfully."
            break
        fi
        sleep 1
    done
}

start() {
    res=$(sudo docker ps | grep minio | grep healthy | wc -l)
    if [ $res -eq 1 ]; then
        echo "MinIO is running."
        exit 0
    fi

    res=$(sudo docker ps -a | grep minio | wc -l)
    if [ $res -eq 1 ]; then
        sudo docker start minio
    else
        run_storage
    fi

    if [ $? -ne 0 ]; then
        echo "Start failed."
        exit 1
    fi

    wait_for_minio_running
}

stop() {
    sudo docker stop minio

    if [ $? -ne 0 ]; then
        echo "Stop failed."
        exit 1
    fi
    echo "Stop successfully."

}

delete_container() {
    res=$(sudo docker ps | grep minio | wc -l)
    if [ $res -eq 1 ]; then
        echo "Please stop Milvus service before delete."
        exit 1
    fi
    sudo docker rm minio
    if [ $? -ne 0 ]; then
        echo "Delete milvus container failed."
        exit 1
    fi
    echo "Delete milvus container successfully."
}

delete() {
    delete_container
    echo "Delete successfully."
}

case $1 in
restart)
    stop
    start
    ;;
start)
    start
    ;;
stop)
    stop
    ;;
delete)
    delete
    ;;
*)
    echo "please use bash run_minio.sh restart|start|stop|delete"
    ;;
esac
