#!/bin/bash

# Start Celery worker in the background
celery -A schedulers worker -l info

# Start Streamlit app
streamlit run main.py --server.port=8501 --server.address=0.0.0.0