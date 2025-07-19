#!/bin/bash
export PYTHONPATH=.
pytest --cov=app tests/
