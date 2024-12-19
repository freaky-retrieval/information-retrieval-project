chmod +x run_milvus.sh
chmod +x run_minio.sh

start()
{
    ./run_minio.sh start

    ./run_milvus.sh start
}

stop()
{
    ./run_milvus.sh stop

    ./run_minio.sh stop
}

delete()
{
    ./run_milvus.sh delete

    ./run_minio.sh delete
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