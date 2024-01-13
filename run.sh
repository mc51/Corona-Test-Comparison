#!/bin/bash
exec .venv/bin/gunicorn wsgi:app -w 2 -b localhost:4444
