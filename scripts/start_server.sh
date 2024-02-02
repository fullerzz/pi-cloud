#!/bin/bash

poetry run uvicorn src.pi_cloud.main:app --log-level trace --access-log --host 0.0.0.0 --reload
