import os
import sys

import subprocess
import multiprocessing

def start_frontend():
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/frontend.log", "w") as f:
        subprocess.run(['npm', 'run', '--prefix=src/vschool/frontend', 'dev'], 
                       stdout=f, stderr=f, shell=True)
        
if __name__ == '__main__':
    start_frontend()