#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.local/bin/env

DATABASE_URL=postgresql://dbanalyzer_zjfi_user:3FHmEgMyH82Ly8Xqu5TSWQ8kk4xgLGm4@dpg-d8jm6ul8nd3s73fq1gbg-a.virginia-postgres.render.com/dbanalyzer_zjfi

make install && psql $DATABASE_URL -f database.sql