import os
import sys
import signal
import argparse

import subprocess
import multiprocessing

from vschool.backend.server import Server

def start_frontend(port=3000):
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/frontend.log", "w", encoding="utf-8") as f:
        subprocess.run(['npm', 'run', '--prefix=src/vschool/frontend', 'dev', '--', f'--port={port}'], 
                       stdout=f, stderr=f, shell=True)

def start_backend(port=5000):
    sys.stdout = open("outputs/backend.log", "w", encoding="utf-8")
    sys.stderr = sys.stdout

    db_url = 'src/vschool/data/test.db'
    server = Server(os.path.abspath(db_url), port)
    server.run()

def main(args):
    def cleanup():
        print("\nShutting down processes...")
        if p_backend.is_alive():
            p_backend.terminate()
            print("Backend server terminated.")
        if p_frontend.is_alive():
            p_frontend.terminate()
            print("Frontend server terminated.")
        sys.exit(0)

    p_backend = multiprocessing.Process(target=start_backend, args=(args.backend_port,))
    p_backend.start()
    print(f"Backend server started on port {args.backend_port}")

    p_frontend = multiprocessing.Process(target=start_frontend, args=(args.frontend_port,))
    p_frontend.start()
    print(f"Frontend server started on port {args.frontend_port}")
    print(f"Access the frontend at http://localhost:{args.frontend_port}")

    try:
        # wait for the processes to finish
        p_backend.join()
        p_frontend.join()
    except KeyboardInterrupt:
        cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frontend_port', type=int, default=3000, help='port to run the frontend server on')
    parser.add_argument('--backend_port', type=int, default=5000, help='port to run the backend server on')
    args = parser.parse_args()

    main(args)
