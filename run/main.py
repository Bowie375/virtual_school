import os
import sys
import signal
import argparse

import subprocess
import multiprocessing

from vschool.backend.server import Server

def start_frontend(control_pipe, port=3000):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    env = os.environ.copy()
    env["FORCE_COLOR"] = "0"

    log_file = open("outputs/frontend.log", "w", encoding="utf-8")
    try:
        proc = subprocess.Popen([
            'npm', 'run', 'dev', '--prefix=src/vschool/frontend', '--', f'--port={port}'],
            stdout=log_file, stderr=log_file, stdin=subprocess.PIPE,
            text=True, env=env, shell=True
        )

        while True:
            if control_pipe.poll():
                msg = control_pipe.recv()
                if msg == "quit":
                    print(f"Frontend server received quit msg, shutting down...")
                    try:
                        proc.stdin.write('y\n')
                        proc.stdin.flush()
                    except Exception as e:
                        print(f"Failed to send quit command: {e}")
                    proc.wait()
                    break
    finally:
        print("Closing frontend log file...")
        log_file.close()


def start_backend(port=5000):
    sys.stdout = open("outputs/backend.log", "w", encoding="utf-8")
    sys.stderr = sys.stdout

    db_url = 'src/vschool/data/test.db'
    server = Server(os.path.abspath(db_url), port)
    server.run()


def main(args):
    def cleanup(frontend_pipe):
        print("\nShutting down processes...")
        if p_backend.is_alive():
            p_backend.terminate()
            print("Backend server terminated.")
        if p_frontend.is_alive():
            frontend_pipe.send("quit")
            print("Sent quit to frontend server.")
            p_frontend.join()
            print("Frontend server terminated.")
        p_backend.join()
        sys.exit(0)

    parent_conn, child_conn = multiprocessing.Pipe()

    p_backend = multiprocessing.Process(target=start_backend, args=(args.backend_port,))
    p_backend.start()
    print(f"Backend server started on port {args.backend_port}")

    p_frontend = multiprocessing.Process(target=start_frontend, args=(child_conn, args.frontend_port))
    p_frontend.start()
    print(f"Frontend server started on port {args.frontend_port}")
    print(f"Access the frontend at http://localhost:{args.frontend_port}")

    try:
        p_backend.join()
        p_frontend.join()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, shutting down...")
        cleanup(parent_conn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frontend_port', type=int, default=3000, help='port to run the frontend server on')
    parser.add_argument('--backend_port', type=int, default=5000, help='port to run the backend server on')
    args = parser.parse_args()

    main(args)