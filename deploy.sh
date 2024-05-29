#!/bin/bash
set -e

# Run Alembic migrations
alembic upgrade head


chmod +x deploy.sh