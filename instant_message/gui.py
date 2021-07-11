from __future__ import print_function

import tkinter as tk
from threading import Thread

from utils4 import register_q, login_q, request_q


class ChatBox:
    def __init__(self, root, my_name, username, send_queue):
        self.username = username
        self.send_queue = send_queue
        self.my_name = my_name

        # Create chat Box
        self.wnd = tk.Toplevel(root)
        self.wnd.title(my_name + " and " + username)

        # Create Frame
        self.frame = tk.Frame(master=self.wnd, width=30, height=20, bg="white")
        self.frame.pack(fill=tk.BOTH)

        # Create Send button
        self.send_btn = tk.Button(master=self.frame,
                                  width=8, height=2,
                                  bg="green", fg="white",
                                  text="Send", font=("Helvetica", 10, "bold"),
                                  command=lambda: self._on_send())
        self.send_btn.pack(fill=tk.BOTH, side='bottom')

        # Also bind 'Enter' key to self._add_message_on_send()
        self.wnd.bind('<Return>', lambda event: self._on_send())

        # Create status label
        self.status_txt = tk.StringVar(value='This is the start of your conversation with ' + self.username + '\n')
        self.status_lbl = tk.Label(master=self.frame,
                                   width=30, height=15,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create message input box
        self.msg_in_entry = tk.Text(master=self.frame,
                                    width=30, height=1,
                                    font=("Helvetica", 15),
                                    bg="white", fg="black")
        self.msg_in_entry.focus_set()
        self.msg_in_entry.pack(fill=tk.BOTH, side=tk.LEFT)

        self.wnd.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_send(self):
        msg = self.msg_in_entry.get("1.0", tk.END).strip()
        if not msg:
            return
        self.msg_in_entry.delete("1.0", tk.END)

        txt = self.status_txt.get()
        txt += self.my_name
        txt += ": "
        txt += msg
        txt += "\n"
        self.status_txt.set(txt)

        self.send_queue.put(("Msg", self.username + "," + msg))

    def _on_closing(self):
        self.wnd.withdraw()


class ClientBox:
    def __init__(self, root, send_queue, receive_queue):
        self.register_action = lambda: print('Registering!')
        self.login_action = lambda: print('Logging In!')
        self.request_action = lambda: print('Requesting Registry!')
        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.root = root
        self.chat_boxes = {}

        # Create message Box
        self.message_wnd = tk.Toplevel(root)
        self.message_wnd.title('Client')

        # Create Ping Frame
        self.reg_frame = tk.Frame(master=self.message_wnd, width=30, height=20, bg="white")
        self.reg_frame.pack(fill=tk.BOTH)

        # Create Register button
        self.register_btn = tk.Button(master=self.reg_frame,
                                      width=8, height=2,
                                      bg="green", fg="white",
                                      text="Register", font=("Helvetica", 10, "bold"),
                                      command=lambda: self._on_register())
        self.register_btn.pack(fill=tk.BOTH)

        # Also bind 'Enter' key to self._add_message_on_send()
        self.message_wnd.bind('<Return>', lambda event: self._on_register())

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to Register...\n')
        self.status_lbl = tk.Label(master=self.reg_frame,
                                   width=30, height=15,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create message input box
        self.msg_in_entry = tk.Text(master=self.reg_frame,
                                    width=30, height=1,
                                    font=("Helvetica", 15),
                                    bg="white", fg="black")
        self.msg_in_entry.focus_set()
        self.msg_in_entry.pack(fill=tk.BOTH, side=tk.LEFT)

        self.message_wnd.protocol("WM_DELETE_WINDOW", self.on_closing)

        # create receive queue polling thread
        self.rxq_worker = Thread(target=lambda: self._process_receive_queue(), daemon=True)
        self.rxq_worker.start()

    def _process_receive_queue(self):
        while True:
            txt = self.status_txt.get()
            msg_type, msg_data = self.receive_queue.get()
            print(msg_type)
            if msg_type == "RegistrationSuccessful":
                txt += "Registration was Successful \n"
                self.status_txt.set(txt)
                self.reg_frame.destroy()
                self._create_login_frame()
            elif msg_type == "RegistrationFailed":
                txt += "Registration Failed \n"
                self.status_txt.set(txt)
            elif msg_type == "LoginSuccessful":
                txt += "Login was Successful \n"
                self.status_txt.set(txt)
                self.login_frame.destroy()
                self._create_request_frame()
            elif msg_type == "LoginFailed":
                txt += "Login Failed \n"
                self.status_txt.set(txt)
            elif msg_type == "UserList":
                clients = msg_data.split(',')
                print(clients)
                self.usr_lstbox.delete(0, tk.END)
                for item in clients:
                    self.usr_lstbox.insert(tk.END, item)
            elif msg_type == "Msg":
                msgs = msg_data.split(',')
                sender = msgs[0]
                msg = msgs[1]
                print("received message ", msg)
                if sender not in self.chat_boxes.keys():
                    self.chat_boxes[sender] = ChatBox(self.root, self.username, sender, self.send_queue)

                txt = self.chat_boxes[sender].status_txt.get()
                txt += sender
                txt += ": "
                txt += msg
                txt += "\n"
                self.chat_boxes[sender].status_txt.set(txt)

    def on_closing(self):
        print("closing")
        self.send_queue.put(("CloseConnection", ""))
        self.message_wnd.destroy()

    def _create_login_frame(self):
        self.message_wnd.title('Client ' + self.username)
        # Create Login Frame
        self.login_frame = tk.Frame(master=self.message_wnd, width=30, height=15, bg="white")
        self.login_frame.pack(fill=tk.BOTH)

        # Create Login button
        self.login_btn = tk.Button(master=self.login_frame,
                                   width=8, height=2,
                                   bg="green", fg="white",
                                   text="Login", font=("Helvetica", 10, "bold"),
                                   command=lambda: self._on_login())
        self.login_btn.pack(fill=tk.BOTH)

        self.message_wnd.bind('<Return>', lambda event: self._on_login())

        # Create status label
        self.status_txt = tk.StringVar(value='Waiting to Login...\n')
        self.status_lbl = tk.Label(master=self.login_frame,
                                   width=30, height=15,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create message input box
        self.msg_in_entry = tk.Text(master=self.login_frame,
                                    width=30, height=1,
                                    font=("Helvetica", 20),
                                    bg="white", fg="black")
        self.msg_in_entry.focus_set()
        self.msg_in_entry.pack(fill=tk.BOTH, side=tk.LEFT)

    def _on_register(self):
        self.register_action()

        msg = self.msg_in_entry.get("1.0", tk.END).strip()
        if not msg:
            return
        self.msg_in_entry.delete("1.0", tk.END)
        self.send_queue.put(("Register", msg))
        self.username = msg

    def _create_request_frame(self):
        # Create request Frame
        self.msg_frame = tk.Frame(master=self.message_wnd, width=30, height=15, bg="white")
        self.msg_frame.pack(fill=tk.BOTH)

        # Create request button
        self.request_btn = tk.Button(master=self.msg_frame,
                                     width=8, height=2,
                                     bg="green", fg="white",
                                     text="Request User Registry", font=("Helvetica", 10, "bold"),
                                     command=lambda: self._on_request())
        self.request_btn.pack(fill=tk.BOTH)

        self.message_wnd.bind('<Return>', lambda event: self._on_request())

        # Create status label
        self.status_txt = tk.StringVar(value='CLIENT REGISTRY\n')
        self.status_lbl = tk.Label(master=self.msg_frame,
                                   width=30, height=3,
                                   textvariable=self.status_txt,
                                   font=("Helvetica", 10),
                                   bg="white", fg="black")
        self.status_lbl.pack(fill=tk.BOTH)

        # Create message output box
        self.usr_lstbox = tk.Listbox(master=self.msg_frame,
                                     font=("Helvetica", 20),
                                     width=30, height=15,
                                     selectforeground='white',
                                     selectbackground='blue',
                                     bg="white", fg="black")
        self.usr_lstbox.pack(fill=tk.BOTH, side=tk.LEFT)

        # Bind usr_lstbox select action to callback
        self.usr_lstbox.bind("<<ListboxSelect>>", lambda event: self._on_select(event))

    def _on_select(self, event):
        sel = event.widget.curselection()
        if sel:
            idx = sel[0]
            data = event.widget.get(idx)
            print(data)
            print(self.chat_boxes.keys())
            if data not in self.chat_boxes.keys():
                self.chat_boxes[data] = ChatBox(self.root, self.username, data, self.send_queue)
            else:
                chatbox = self.chat_boxes[data]
                chatbox.wnd.deiconify()

    def _on_login(self):
        self.login_action()

        msg = self.msg_in_entry.get("1.0", tk.END).strip()
        if not msg:
            return
        self.msg_in_entry.delete("1.0", tk.END)
        self.send_queue.put(("Login", msg))

    def _on_request(self):
        self.request_action()
        self.send_queue.put(("Request", ""))


class ServerBox:
    def __init__(self, root, register_cv, login_cv, request_users_cv, message_queue):
        self.register_action = lambda: print('Registering User!')
        self.login_action = lambda: print('Logging in User!')
        self.request_action = lambda: print('Sending user registry!')

        self.register_cv = register_cv
        self.login_cv = login_cv
        self.request_users_cv = request_users_cv

        self.message_queue = message_queue

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

        # Create and start message queue worker
        self.msg_q_worker = Thread(target=lambda: self._process_message(), daemon=True)
        self.msg_q_worker.start()

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

    def _process_message(self):
        while True:
            sender, receiver = self.message_queue.get()
            if sender:
                status = "Sending message from " + sender + " to " + receiver
                txt = self.status_txt.get()
                txt += status
                txt += ' \n'
                self.status_txt.set(txt)
