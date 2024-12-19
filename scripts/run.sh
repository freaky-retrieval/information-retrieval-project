chmod +x ./scripts/run_milvus.sh
chmod +x ./scripts/run_minio.sh

start()
{
    ./scripts/run_minio.sh start

    ./scripts/run_milvus.sh start
}

stop()
{
    ./scripts/run_milvus.sh stop

    ./scripts/run_minio.sh stop
}

delete()
{
    ./scripts/run_milvus.sh delete

    ./scripts/run_minio.sh delete
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