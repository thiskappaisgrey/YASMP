#!/usr/bin/env python3
from app import create_app

yasmp = create_app()

if __name__ == "__main__":
    yasmp.run(host="localhost")
