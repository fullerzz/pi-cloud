#!/bin/bash

poetry run uvicorn src.pi_cloud.main:app --log-level debug --reload
