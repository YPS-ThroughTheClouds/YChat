from __future__ import print_function

import tkinter as tk
from queue import Queue
from threading import Thread
from time import sleep


class Registry:
    def __init__(self, root, usr_lst, on_select):
        self.usr_lst = usr_lst
        self.on_select = on_select

        # Create main window
        self.usr_wnd = tk.Toplevel(root)
        self.usr_wnd.title('User Registry')

        # Create output frame
        self.usr_frame = tk.Frame(master=self.usr_wnd, width=50, height=20, bg="white")
        self.usr_frame.pack(fill=tk.BOTH)

        # Create message output box
        self.usr_lstbox = tk.Listbox(master=self.usr_frame,
                                     font=("Helvetica", 20),
                                     width=50, height=20,
                                     selectforeground='white',
                                     selectbackground='blue',
                                     bg="white", fg="black")
        self.usr_lstbox.pack(fill=tk.BOTH, side=tk.LEFT)

        # Bind usr_lstbox select action to callback
        self.usr_lstbox.bind("<<ListboxSelect>>", lambda event: self._on_select(event))

        # Create and start message worker
        self.usr_worker = Thread(target=lambda: self._process_usernames(), daemon=True)
        self.usr_worker.start()

    def _process_usernames(self):
        while True:
            self.usr_lstbox.insert(tk.END, self.usr_lst.get())

    def _on_select(self, event):
        sel = event.widget.curselection()
        if sel:
            idx = sel[0]
            data = event.widget.get(idx)
            self.on_select(data)


class UserWriter(Thread):
    def __init__(self, usr_lst):
        Thread.__init__(self)
        self.usr_list = usr_lst
        self.do_run = True

    def run(self):
        i = 0
        while self.do_run:
            sleep(1)
            self.usr_list.put("usr" + str(i))
            i += 1

    def stop(self):
        self.do_run = False


if __name__ == "__main__":
    usr_list = Queue()
    writer = UserWriter(usr_list)

    writer.start()

    rt = tk.Tk()
    box = Registry(rt, usr_list, lambda x: print(x))
    rt.withdraw()
    rt.mainloop()

    writer.stop()
    writer.join()
