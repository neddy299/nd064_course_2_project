import os

from app import run_app


if __name__ == '__main__':
  run_app(os.getenv("APP_ENV") or "test")