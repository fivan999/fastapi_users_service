#!/bin/sh

set -e

# Activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here
alembic upgrade head

# Evaluating passed command:
exec "$@"