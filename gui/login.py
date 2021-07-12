from __future__ import print_function

import tkinter as tk

from utils import noop


class Login:
    def __init__(self, root, login_action=noop):
        self.login_action = login_action

        # Create login window
        self.login_wnd = tk.Toplevel(root)
        self.login_wnd.title('Login')

        # Create login frame
        self.login_frame = tk.Frame(master=self.login_wnd, width=100, height=50, bg="white")
        self.login_frame.pack(fill=tk.BOTH)

        # Create username entry
        self.username_entry = tk.Entry(master=self.login_frame,
                                       width=120,
                                       font=("Helvetica", 20),
                                       bg="white", fg="black")
        self.username_entry.focus_set()
        self.username_entry.pack(fill=tk.BOTH, side=tk.LEFT)

        # Create login button
        self.login_btn = tk.Button(master=self.login_frame,
                                   width=8, height=2,
                                   bg="blue", fg="black",
                                   text="Login", font=("Helvetica", 20),
                                   command=lambda: self._on_login())
        self.login_btn.pack(fill=tk.BOTH, side=tk.LEFT)

        # Also bind 'Enter' key to self._on_login()
        self.login_btn.bind('<Return>', lambda event: self._on_login())

    def _on_login(self):
        username = self.username_entry.get().strip()
        if not username:
            return
        self.username_entry.delete(0, tk.END)
        self.login_action(username)


if __name__ == "__main__":
    rt = tk.Tk()
    login = Login(rt, lambda x: print(x))
    rt.withdraw()
    rt.mainloop()
