#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

delete FROM voto_voto;

delete FROM voto_votante;

delete FROM voto_candidato;

# Apply any outstanding database migrations
python manage.py migrate