#!/bin/bash

# Function to check if a container exists and perform action
manage_containers() {
  local action="$1" # "start" or "stop"
  local container_name="$2"

  echo "Checking container '$container_name' for action: $action"

  if sudo docker container inspect "$container_name" > /dev/null 2>&1; then
    case "$action" in
      "start")
        echo "Container '$container_name' found. Starting..."
        sudo docker start "$container_name"
        ;;
      "stop")
        echo "Container '$container_name' found. Stopping..."
        sudo docker stop "$container_name"
        ;;
      *)
        echo "Invalid action: $action. Must be 'start' or 'stop'."
        return 1
        ;;
    esac
  elif [[ "$action" == "start" ]]; then
    echo "Container '$container_name' not found. Creating..."
    case "$container_name" in
      "mongo-db")
        sudo docker run -d --name "$container_name" -p 27017:27017 mongo
        ;;
      "redis")
        sudo docker run -d --name "$container_name" -p 6379:6379 redis
        ;;
      "minio")
        sudo docker run -d -p 9000:9000 -p 9001:9001 --name "$container_name" -v "$HOME/minio/data:/data" -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" quay.io/minio/minio server /data --console-address ":9001"
        ;;
      *)
        echo "Unknown container name: $container_name"
        return 1
        ;;
    esac
  else
      echo "Container '$container_name' not found, nothing to stop."
  fi

  echo "Container '$container_name' handled."
}


# Main script logic

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 {start|stop}"
  exit 1
fi

command="$1" # Removed 'local'
if [[ "$command" != "start" && "$command" != "stop" ]]; then
  echo "Invalid command: $command. Must be 'start' or 'stop'."
  exit 1
fi

# Manage containers
manage_containers "$command" "mongo-db"
manage_containers "$command" "redis"
manage_containers "$command" "minio"

echo "All container actions completed"