import tkinter as tk
from tkinter import messagebox
import pymysql


class Bank:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")

        scrn_width = self.root.winfo_screenwidth()
        scrn_height = self.root.winfo_screenheight()

        self.root.geometry(f"{scrn_width}x{scrn_height}+0+0")

        self.mainFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="ridge")
        self.mainFrame.place(x=400, y=90, width=450, height=550)

        mainlabel = tk.Label(self.root, text="Bank Account Management System", font=("Arial", 40, "bold"), bg="red",
                             bd=5, relief="groove")
        mainlabel.pack(side="top", fill="x")

        self.create_main_buttons()

    def create_main_buttons(self):
        openAcbtn = tk.Button(self.mainFrame, command=self.openAc, width=20, text="Open Your Account", bg="orange",
                              bd=3,
                              relief="raised", font=("Arial", 20, "bold"))
        openAcbtn.grid(row=0, column=0, padx=40, pady=70)

        depbtn = tk.Button(self.mainFrame, command=self.deposit, width=20, text="Deposit", bg="orange", bd=3,
                           relief="raised",
                           font=("Arial", 20, "bold"))
        depbtn.grid(row=1, column=0, padx=40, pady=70)

        withbtn = tk.Button(self.mainFrame, command=self.wd, width=20, text="Withdraw", bg="orange", bd=3,
                            relief="raised",
                            font=("Arial", 20, "bold"))
        withbtn.grid(row=2, column=0, padx=40, pady=70)

        self.current_frame = None

    def switch_frame(self, new_frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame_class(self.root)

    def openAc(self):
        self.switch_frame(OpenAccountFrame)

    def deposit(self):
        self.switch_frame(DepositFrame)

    def wd(self):
        self.switch_frame(WithdrawFrame)


class OpenAccountFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="light gray", bd=5, relief="ridge")
        self.place(x=400, y=90, width=450, height=550)

        tk.Label(self, text="Enter Name:", bg="light gray", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20,
                                                                                             pady=30)
        self.uNameIn = tk.Entry(self, width=15, font=("Arial", 15))
        self.uNameIn.grid(row=0, column=1, padx=5, pady=30)

        tk.Label(self, text="Enter Password:", bg="light gray", font=("Arial", 15, "bold")).grid(row=1, column=0,
                                                                                                 padx=20, pady=30)
        self.uPwIn = tk.Entry(self, width=15, font=("Arial", 15), show='*')
        self.uPwIn.grid(row=1, column=1, padx=5, pady=30)

        tk.Label(self, text="Confirm Password:", bg="light gray", font=("Arial", 15, "bold")).grid(row=2, column=0,
                                                                                                   padx=20, pady=30)
        self.confirmIn = tk.Entry(self, width=15, font=("Arial", 15), show='*')
        self.confirmIn.grid(row=2, column=1, padx=5, pady=30)

        tk.Button(self, command=self.insert, text="Confirm", width=10, bg="orange", bd=3,
                  relief="raised", font=("Arial", 15, "bold")).grid(row=3, column=0, padx=40, pady=120)

        tk.Button(self, command=self.close_frame, text="Close", width=10, bg="orange", bd=3,
                  relief="raised", font=("Arial", 15, "bold")).grid(row=3, column=1, padx=40, pady=120)

    def close_frame(self):
        self.destroy()

    def insert(self):
        uName = self.uNameIn.get()
        uPW = self.uPwIn.get()
        confirm = self.confirmIn.get()

        if not uName or not uPW or not confirm:
            messagebox.showerror("Error", "All fields must be filled out!")
            return

        if uPW != confirm:
            messagebox.showerror("Error", "Both passwords must be the same!")
            return

        try:
            con = pymysql.connect(host="localhost", user="root", passwd="ROOT", database="banksystem")
            cur = con.cursor()
            cur.execute("INSERT INTO account (userName, userPw) VALUES (%s, %s)", (uName, uPW))
            con.commit()
            messagebox.showinfo("Success", "Account opened successfully!")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if con:
                con.close()

    def clear_fields(self):
        self.uNameIn.delete(0, tk.END)
        self.uPwIn.delete(0, tk.END)
        self.confirmIn.delete(0, tk.END)


class DepositFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="light gray", bd=5, relief="ridge")
        self.place(x=400, y=90, width=450, height=550)

        tk.Label(self, text="User Name:", bg="light gray", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20,
                                                                                            pady=30)
        self.NameIn = tk.Entry(self, width=15, font=("Arial", 15))
        self.NameIn.grid(row=0, column=1, padx=5, pady=30)

        tk.Label(self, text="Enter Amount:", bg="light gray", font=("Arial", 15, "bold")).grid(row=1, column=0, padx=20,
                                                                                               pady=30)
        self.amountIn = tk.Entry(self, width=15, font=("Arial", 15))
        self.amountIn.grid(row=1, column=1, padx=5, pady=30)

        tk.Button(self, command=self.deposit_fun, text="Deposit", width=10, bg="orange", bd=3,
                  relief="raised", font=("Arial", 15, "bold")).grid(row=2, column=0, padx=40, pady=150)

        tk.Button(self, command=self.close_frame, text="Close", width=10, bg="orange", bd=3,
                  relief="raised", font=("Arial", 15, "bold")).grid(row=2, column=1, padx=40, pady=150)

    def close_frame(self):
        self.destroy()

    def deposit_fun(self):
        name = self.NameIn.get()
        amount_str = self.amountIn.get()

        if not amount_str.isdigit() or int(amount_str) <= 0:
            messagebox.showerror("Error", "Enter a valid positive amount.")
            return

        amount = int(amount_str)

        try:
            con = pymysql.connect(host="localhost", user="root", passwd="ROOT", database="banksystem")
            cur = con.cursor()
            cur.execute("SELECT balance FROM account WHERE userName=%s", name)
            data = cur.fetchone()

            if data:
                balance = data[0] if data[0] is not None else 0
                update = balance + amount
                cur.execute("UPDATE account SET balance=%s WHERE userName=%s", (update, name))
                con.commit()
                messagebox.showinfo("Success", "Amount updated successfully!")
            else:
                messagebox.showerror("Error", "Invalid customer name")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if con:
                con.close()


class WithdrawFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="light gray", bd=5, relief="ridge")
        self.place(x=400, y=90, width=450, height=550)

        tk.Label(self, text="User Name:", bg="light gray", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20,
                                                                                            pady=30)
        self.cNameIn = tk.Entry(self, width=15, font=("Arial", 15))
        self.cNameIn.grid(row=0, column=1, padx=5, pady=30)

        tk.Label(self, text="Enter Password:", bg="light gray", font=("Arial", 15, "bold")).grid(row=1, column=0,
                                                                                                 padx=20, pady=30)
        self.cPWIn = tk.Entry(self, width=15, font=("Arial", 15), show='*')
        self.cPWIn.grid(row=1, column=1, padx=5, pady=30)

        tk.Label(self, text="Enter Amount:", bg="light gray", font=("Arial", 15, "bold")).grid(row=2, column=0, padx=20,
                                                                                               pady=30)
        self.wdIn = tk.Entry(self, width=15, font=("Arial", 15))
        self.wdIn.grid(row=2, column=1, padx=5, pady=30)

        tk.Button(self, command=self.wd_fun, text="Withdraw", width=10, bg="orange", bd=3,
                  relief="raised", font=("Arial", 15, "bold")).grid(row=3, column=0, padx=40, pady=150)

        tk.Button(self, command=self.close_frame, text="Close", width=10, bg="orange", bd=3,
                  relief="raised", font=("Arial", 15, "bold")).grid(row=3, column=1, padx=40, pady=150)

    def close_frame(self):
        self.destroy()

    def wd_fun(self):
        name = self.cNameIn.get()
        pw = self.cPWIn.get()
        amount_str = self.wdIn.get()

        if not amount_str.isdigit() or int(amount_str) <= 0:
            messagebox.showerror("Error", "Enter a valid positive amount.")
            return

        amount = int(amount_str)

        try:
            con = pymysql.connect(host="localhost", user="root", passwd="ROOT", database="banksystem")
            cur = con.cursor()
            cur.execute("SELECT userPw, balance FROM account WHERE userName=%s", name)
            data = cur.fetchone()

            if data:
                if data[0] == pw:
                    if data[1] >= amount:
                        update = data[1] - amount
                        cur.execute("UPDATE account SET balance=%s WHERE userName=%s", (update, name))
                        con.commit()
                        messagebox.showinfo("Success", "Withdrawal successful!")
                    else:
                        messagebox.showerror("Error", "Insufficient funds.")
                else:
                    messagebox.showerror("Error", "Invalid password.")
            else:
                messagebox.showerror("Error", "Invalid customer name.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if con:
                con.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = Bank(root)
    root.mainloop()
