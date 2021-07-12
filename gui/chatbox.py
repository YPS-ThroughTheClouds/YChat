from __future__ import print_function

import tkinter as tk
from queue import Queue
from threading import Thread
from time import sleep


class ChatBox:
    def __init__(self, root, username, send_queue, recv_queue):
        self.username = username
        self.send_queue = send_queue
        self.disp_queue = recv_queue

        # Create main window
        self.chat_wnd = tk.Toplevel(root)
        self.chat_wnd.title('Chat Window')

        # Create output frame
        self.out_frame = tk.Frame(master=self.chat_wnd, width=100, height=50, bg="white")
        self.out_frame.pack(fill=tk.BOTH)

        # Create message output box
        self.msg_out_lbl = tk.Label(master=self.out_frame,
                                    font=("Helvetica", 20),
                                    anchor='nw', justify=tk.LEFT,
                                    width=100, height=50,
                                    bg="white", fg="black")
        self.msg_out_lbl.pack(fill=tk.BOTH, side=tk.LEFT)

        # Create input frame
        self.in_frame = tk.Frame(master=self.chat_wnd, width=100, height=2, bg="white")
        self.in_frame.pack(fill=tk.BOTH)

        # Create message input box
        self.msg_in_entry = tk.Text(master=self.in_frame,
                                    width=120, height=1,
                                    font=("Helvetica", 20),
                                    bg="white", fg="black")
        self.msg_in_entry.focus_set()
        self.msg_in_entry.pack(fill=tk.BOTH, side=tk.LEFT)

        # Create message send button
        self.msg_send_btn = tk.Button(master=self.in_frame,
                                      width=6, height=2,
                                      bg="blue", fg="black",
                                      text="Send", font=("Helvetica", 20),
                                      command=lambda: self._on_send())
        self.msg_send_btn.pack(fill=tk.BOTH, side=tk.LEFT)

        # Also bind 'Enter' key to self._add_message_on_send()
        self.chat_wnd.bind('<Return>', lambda event: self._on_send())

        # Create and start message worker
        self.msg_worker = Thread(target=lambda: self._process_messages(), daemon=True)
        self.msg_worker.start()

    def _process_messages(self):
        while True:
            self.msg_out_lbl["text"] += "{}: {}\n".format(*self.disp_queue.get())

    def _on_send(self):
        msg = self.msg_in_entry.get("1.0", tk.END).strip()
        if not msg:
            return
        self.msg_in_entry.delete("1.0", tk.END)
        self.send_queue.put((self.username, msg))
        self.disp_queue.put((self.username, msg))


class Sender(Thread):
    def __init__(self, send_queue):
        Thread.__init__(self)
        self.send_queue = send_queue
        self.do_run = True

    def run(self):
        while self.do_run:
            username, msg = self.send_queue.get()
            print('Sending message from {}: {}'.format(username, msg))

    def stop(self):
        self.do_run = False


class Receiver(Thread):
    def __init__(self, recv_queue):
        Thread.__init__(self)
        self.recv_queue = recv_queue
        self.do_run = True

    def run(self):
        while self.do_run:
            sleep(1)
            self.recv_queue.put(('you', 'Hey are you in there?'))

    def stop(self):
        self.do_run = False


if __name__ == "__main__":
    send = Queue()
    recv = Queue()

    sender = Sender(send)
    receiver = Receiver(recv)

    sender.start()
    receiver.start()

    rt = tk.Tk()
    box = ChatBox(rt, "me", send, recv)
    rt.withdraw()
    rt.mainloop()

    sender.stop()
    receiver.stop()

    sender.join()
    receiver.join()
