from __future__ import print_function

import tkinter as tk
from threading import Thread, Condition
import time

class Client1Box:
    def __init__(self, root, ping_action, pong_action, pong_cv, ping_queue):
        self.ping_action = ping_action
        self.pong_action = pong_action
        self.pong_cv = pong_cv
        self.ping_queue = ping_queue

        # Create PingBox
        self.ping_wnd = tk.Toplevel(root)
        self.ping_wnd.title('Client 1')

        # Create Ping Frame
        self.ping_frame = tk.Frame(master=self.ping_wnd, width=50, height=25, bg="white")
        self.ping_frame.pack(fill=tk.BOTH)

        # Create Ping button
        self.ping_btn = tk.Button(master=self.ping_frame,
                                  width=8, height=2,
                                  bg="green", fg="white",
                                  text="Ping", font=("Helvetica", 10, "bold"),
                                  command=lambda: self._on_ping())
        self.ping_btn.pack(fill=tk.BOTH)

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to send Ping message...\n')
        self.status_lbl = tk.Label(master=self.ping_frame,
                                   width=50, height=15,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create and start message worker
        self.pong_worker = Thread(target=lambda: self._process_pong(), daemon=True)
        self.pong_worker.start()

    def _on_ping(self):
        self.ping_action()
        self.ping_queue.put("Ping")

        txt = self.status_txt.get()
        txt += 'Sent Ping message!\n'
        self.status_txt.set(txt)

    def _process_pong(self):
        while True:
            with self.pong_cv:
                self.pong_cv.wait()
            self.pong_action()
            txt = self.status_txt.get()
            txt += 'Received Pong message!\n'
            self.status_txt.set(txt)


class Client2Box:
    def __init__(self, root, ping_action, pong_action, ping_cv, pong_queue):
        self.ping_action = ping_action
        self.pong_action = pong_action
        self.ping_cv = ping_cv
        self.pong_queue = pong_queue

        # Create PongBox
        self.pong_wnd = tk.Toplevel(root)
        self.pong_wnd.title('Client 2')

        # Create Pong Frame
        self.pong_frame = tk.Frame(master=self.pong_wnd, width=50, height=25, bg="white")
        self.pong_frame.pack(fill=tk.BOTH)

        # Create Ping button
        self.pong_btn = tk.Button(master=self.pong_frame,
                                  width=8, height=2,
                                  bg="green", fg="white",
                                  text="Pong", font=("Helvetica", 10, "bold"),
                                  command=lambda: self._on_pong())
        self.pong_btn.pack(fill=tk.BOTH)

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to send Pong message...\n')
        self.status_lbl = tk.Label(master=self.pong_frame,
                                   width=50, height=15,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create and start message worker
        self.ping_worker = Thread(target=lambda: self._process_ping(), daemon=True)
        self.ping_worker.start()

    def _on_pong(self):
        self.pong_action()
        self.pong_queue.put("Pong")

        txt = self.status_txt.get()
        txt += 'Sent Pong message!\n'
        self.status_txt.set(txt)

    def _process_ping(self):
        while True:
            with self.ping_cv:
                self.ping_cv.wait()
            self.ping_action()
            txt = self.status_txt.get()
            txt += 'Received Ping message!\n'
            self.status_txt.set(txt)

class ServerBox:
    def __init__(self, root, ping_action, pong_action, ping_recvd, pong_recvd):
        self.ping_action = ping_action
        self.pong_action = pong_action
        self.ping_recvd = ping_recvd
        self.pong_recvd = pong_recvd

        # Create PongBox
        self.pong_wnd = tk.Toplevel(root)
        self.pong_wnd.title('Server')

        # Create Pong Frame
        self.pong_frame = tk.Frame(master=self.pong_wnd, width=50, height=25, bg="white")
        self.pong_frame.pack(fill=tk.BOTH)

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to receive Ping message...\n')
        self.status_lbl = tk.Label(master=self.pong_frame,
                                   width=50, height=15,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create and start message worker
        self.ping_worker = Thread(target=lambda: self._process_ping(), daemon=True)
        self.ping_worker.start()

        # Create and start message worker
        self.pong_worker = Thread(target=lambda: self._process_pong(), daemon=True)
        self.pong_worker.start()

    def _process_ping(self):
        while True:
            with self.ping_recvd:
                self.ping_recvd.wait()

            txt = self.status_txt.get()
            txt += 'Received Ping message and forwarding it\n'
            self.status_txt.set(txt)

            self.ping_action()

    def _process_pong(self):
        while True:
            with self.pong_recvd:
                self.pong_recvd.wait()

            txt = self.status_txt.get()
            txt += 'Received Pong message and forwarding it\n'
            self.status_txt.set(txt)

            self.pong_action()
