import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'web'))
from app import run_app

if __name__ == "__main__":
    run_app()