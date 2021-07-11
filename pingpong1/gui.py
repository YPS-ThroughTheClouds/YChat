from __future__ import print_function

import tkinter as tk
from threading import Thread, Condition
import time


class ClientBox:
    def __init__(self, root, ping_action, ping_sent, pong_recvd):
        self.ping_action = ping_action
        self.ping_sent = ping_sent
        self.pong_recvd = pong_recvd

        # Create PingBox
        self.ping_wnd = tk.Toplevel(root)
        self.ping_wnd.title('Client')

        # Create Ping Frame
        self.ping_frame = tk.Frame(master=self.ping_wnd, width=50, height=30, bg="white")
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
        with self.ping_sent:
            self.ping_sent.notify()
        txt = self.status_txt.get()
        txt += 'Sent Ping message, waiting to receive Pong message...\n'
        self.status_txt.set(txt)

    def _process_pong(self):
        while True:
            with self.pong_recvd:
                self.pong_recvd.wait()
            txt = self.status_txt.get()
            txt += 'Received Pong message, all done!\n'
            self.status_txt.set(txt)


class ServerBox:
    def __init__(self, root, ping_action, ping_recvd, pong_sent):
        self.ping_action = ping_action
        self.ping_recvd = ping_recvd
        self.pong_sent = pong_sent

        # Create PongBox
        self.pong_wnd = tk.Toplevel(root)
        self.pong_wnd.title('Server')

        # Create Pong Frame
        self.pong_frame = tk.Frame(master=self.pong_wnd, width=50, height=30, bg="white")
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

    def _process_ping(self):
        while True:
            with self.ping_recvd:
                self.ping_recvd.wait()

            time.sleep(0.75)

            txt = self.status_txt.get()
            txt += 'Received Ping message, waiting to send Pong message...\n'
            self.status_txt.set(txt)

            self.ping_action()

            time.sleep(0.75)

            with self.pong_sent:
                self.pong_sent.notify()

            txt = self.status_txt.get()
            txt += 'Sending Pong message, all done!\n'
            self.status_txt.set(txt)

    def _process_pong(self):
        while True:
            with self.pong_sent:
                self.pong_sent.wait()

            txt = self.status_txt.get()
            txt += 'Sent Pong message, all done!\n'
            self.status_txt.set(txt)
