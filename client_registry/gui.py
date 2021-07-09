from __future__ import print_function
import queue

import tkinter as tk
from threading import Thread, Condition
from time import sleep
from utils3 import register_q, login_q, request_q 


class ClientBox:
    def __init__(self, root, button_cv, completed_cv, mutex, action_flags, send_queue, receive_queue):
        self.register_action = lambda: print('Registering!')
        self.login_action = lambda: print('Logging In!')
        self.request_action = lambda: print('Requesting Registry!')
        self.button_cv = button_cv
        self.completed_cv = completed_cv
        self.mutex = mutex
        self.action_flags = action_flags
        self.send_queue = send_queue
        self.receive_queue = receive_queue

        # Create message Box
        self.message_wnd = tk.Toplevel(root)
        self.message_wnd.title('Client')

        # Create Ping Frame
        self.reg_frame = tk.Frame(master=self.message_wnd, width=50, height=25, bg="white")
        self.reg_frame.pack(fill=tk.BOTH)

        # Create Register button
        self.register_btn = tk.Button(master=self.reg_frame,
                                  width=8, height=2,
                                  bg="blue", fg="black",
                                  text="Register", font=("Helvetica", 10),
                                  command=lambda: self._on_register())
        self.register_btn.pack(fill=tk.BOTH)


        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to Register...\n')
        self.status_lbl = tk.Label(master=self.reg_frame,
                                   width=50, height=25,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create message input box
        self.msg_in_entry = tk.Text(master=self.reg_frame,
                                    width=50, height=1,
                                    font=("Helvetica", 15),
                                    bg="white", fg="black")
        self.msg_in_entry.focus_set()
        self.msg_in_entry.pack(fill=tk.BOTH, side=tk.LEFT)

        # # Create and start message worker
        # self.pong_worker = Thread(target=lambda: self._process_pong(), daemon=True)
        # self.pong_worker.start()

    def _create_login_frame(self):
        # Create Login Frame
        self.login_frame = tk.Frame(master=self.message_wnd, width=50, height=25, bg="white")
        self.login_frame.pack(fill=tk.BOTH)

        # Create Login button
        self.login_btn = tk.Button(master=self.login_frame,
                                  width=8, height=2,
                                  bg="blue", fg="black",
                                  text="Login", font=("Helvetica", 10),
                                  command=lambda: self._on_login())
        self.login_btn.pack(fill=tk.BOTH)

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to Login...\n')
        self.status_lbl = tk.Label(master=self.login_frame,
                                   width=50, height=25,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create message input box
        self.msg_in_entry = tk.Text(master=self.login_frame,
                                    width=50, height=1,
                                    font=("Helvetica", 20),
                                    bg="white", fg="black")
        self.msg_in_entry.focus_set()
        self.msg_in_entry.pack(fill=tk.BOTH, side=tk.LEFT)

    def _on_register(self):
        self.register_action()
        
        with self.mutex:
            self.action_flags[0] = True
        
        msg = self.msg_in_entry.get("1.0", tk.END).strip()
        if not msg:
            return
        self.msg_in_entry.delete("1.0", tk.END)
        self.send_queue.put(msg)

        with self.button_cv:
            self.button_cv.notify()

        with self.completed_cv:
            self.completed_cv.wait()
        
        msg = self.receive_queue.get()
        txt = self.status_txt.get()
        txt += msg
        txt += '\n'
        self.status_txt.set(txt)

        if msg == "Registration was successful!":    
            self.reg_frame.destroy()
            self._create_login_frame()

    def _create_request_frame(self):
        # Create request Frame
        self.msg_frame = tk.Frame(master=self.message_wnd, width=50, height=25, bg="white")
        self.msg_frame.pack(fill=tk.BOTH)

        # Create request button
        self.request_btn = tk.Button(master=self.msg_frame,
                                  width=8, height=2,
                                  bg="blue", fg="black",
                                  text="Request User Registry", font=("Helvetica", 10),
                                  command=lambda: self._on_request())
        self.request_btn.pack(fill=tk.BOTH)

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to Request Registry...\n')
        self.status_lbl = tk.Label(master=self.msg_frame,
                                   width=50, height=25,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)
    
    def _on_login(self):
        self.login_action()
        with self.mutex:
            self.action_flags[1] = True
        
        msg = self.msg_in_entry.get("1.0", tk.END).strip()
        if not msg:
            return
        self.msg_in_entry.delete("1.0", tk.END)
        self.send_queue.put(msg)

        with self.button_cv:
            self.button_cv.notify()

        with self.completed_cv:
            self.completed_cv.wait()

        msg = self.receive_queue.get()
        txt = self.status_txt.get()
        txt += msg
        txt += '\n'
        self.status_txt.set(txt)

        if msg == "Login was successful!":    
            self.login_frame.destroy()
            self._create_request_frame()
    
    def _on_request(self):
        self.request_action()
        with self.mutex:
            self.action_flags[2] = True

        with self.button_cv:
            self.button_cv.notify()

        with self.completed_cv:
            self.completed_cv.wait()

        txt = self.status_txt.get()
        txt = 'Client Registry \n'
        
        msg = self.receive_queue.get()
        clients = msg.split(',') 
        print(clients)
        for item in clients:
            txt += item
            txt += '\n'

        self.status_txt.set(txt)


class ServerBox:
    def __init__(self, root, register_cv, login_cv, request_users_cv):
        self.register_action = lambda: print('Registering User!')
        self.login_action = lambda: print('Logging in User!')
        self.request_action = lambda: print('Sending user registry!')

        self.register_cv = register_cv
        self.login_cv = login_cv
        self.request_users_cv = request_users_cv

        # Create status box
        self.status_wnd = tk.Toplevel(root)
        self.status_wnd.title('Server')

        # Create status Frame
        self.status_frame = tk.Frame(master=self.status_wnd, width=50, height=25, bg="white")
        self.status_frame.pack(fill=tk.BOTH)

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to receive messages...\n')
        self.status_lbl = tk.Label(master=self.status_frame,
                                   width=50, height=25,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create and start register worker
        self.register_worker = Thread(target=lambda: self._process_register(), daemon=True)
        self.register_worker.start()

        # Create and start login worker
        self.login_worker = Thread(target=lambda: self._process_login(), daemon=True)
        self.login_worker.start()

        # Create and start request_users worker
        self.request_users_worker = Thread(target=lambda: self._process_request_users(), daemon=True)
        self.request_users_worker.start()

    def _process_register(self):
        while True:
            with self.register_cv:
                self.register_cv.wait()

            msg = register_q.get()
            txt = self.status_txt.get()
            txt += msg
            txt += ' \n'
            self.status_txt.set(txt)

            self.register_action()

    def _process_login(self):
        while True:
            with self.login_cv:
                self.login_cv.wait()

            msg = login_q.get()
            txt = self.status_txt.get()
            txt += msg
            txt += ' \n'
            self.status_txt.set(txt)

            self.login_action()
    
    def _process_request_users(self):
        while True:
            with self.request_users_cv:
                self.request_users_cv.wait()

            msg = request_q.get()
            txt = self.status_txt.get()
            txt += msg
            txt += ' \n'
            self.status_txt.set(txt)

            self.request_action()

