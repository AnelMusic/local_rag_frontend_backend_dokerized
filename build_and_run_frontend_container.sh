#!/bin/bash
set -e

cd frontend || exit 1

docker build -t frontend .

docker run -p 8501:8501 --env-file ./.env frontend
