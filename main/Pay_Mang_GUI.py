# Payment Manager Graphic User Interface
# v3

from tkinter import *
import tkinter.ttk as ttk
import Controllers

Controllers.chk_db()



class Searcher:
    def __init__(self, root, parent):
        for child in parent.winfo_children():
            child.destroy()

        main_frm = ttk.Frame(parent, padding=10)
        main_frm.grid( row=0, column=0 )
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        ttk.Label(main_frm, text='Dirección: ').grid(row=1, column=1, sticky=E)

        self.addr = StringVar()
        addr_ent = ttk.Entry(main_frm, width=15, textvariable=self.addr)
        addr_ent.grid( row=1, column=2, sticky=(W, E) )

        ttk.Button(main_frm, text='Buscar', command=self.search_addr).grid(row=2, column=2)

        self.fnd_frm = ttk.Frame(main_frm, relief='sunken', width=600, height=400, borderwidth=5)
        self.fnd_frm.grid(row=4, column=1, columnspan=2)
        self.fnd_frm.grid_propagate(0)

        for child in main_frm.winfo_children():
            child.grid_configure(padx=10, pady=10)

        addr_ent.focus()
        root.bind('<Return>', self.search_addr)

        
    def search_addr(self, *args):
        try:
            value = self.addr.get()
        except:
            print('error ----> ')
            return
        try:
            value = value.lower()
            value = value.capitalize()
        except:
            print('Error -----> ')
            return
        addr_found = Controllers.addr_search(value)
        if not addr_found:
            Not_Found(self.fnd_frm)
        else:
            pay_found = Controllers.pay_search(addr_found[0][0]) # del
            Founder(self.fnd_frm, (addr_found, pay_found)) # del pay_found



class Founder:
    def __init__(self, parent, found):
        for child in parent.winfo_children():
            child.destroy()

        (self.addr_info, *self.pay_info) = found # mod
        self.addr_info = self.addr_info[0]
        self.pay_info = self.pay_info[0] # del
        (addr_id, db_addr, db_cost, db_balance) = self.addr_info
        last_info = Controllers.last_pay(addr_id)
        (last_pay, last_day) = last_info
        
        main_frm = ttk.Frame(parent, padding=10)
        main_frm.grid( row=0, column=0 )
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        ttk.Label(main_frm, text='Información encontrada: ').grid( row=1, column=1, sticky=(W, E) )

        ttk.Label(main_frm, text= 'Dirección : ').grid(row=3, column=1)
        ttk.Label(main_frm, text= db_addr).grid(row=3, column=2)

        ttk.Label(main_frm, text= 'Costo : ').grid(row=4, column=1)
        ttk.Label(main_frm, text= f'${db_cost}').grid(row=4, column=2)

        ttk.Label(main_frm, text= 'Balance : ').grid(row=5, column=1)
        ttk.Label (main_frm, text= f'${db_balance}').grid(row=5, column=2)

        ttk.Label(main_frm, text= 'Último pago en : ').grid(row=6, column=1)
        ttk.Label(main_frm, text= last_day).grid(row=6, column=2)

        ttk.Label(main_frm, text= 'Último pago por : ').grid(row=7, column=1)
        ttk.Label(main_frm, text= f'${last_pay}').grid(row=7, column=2)

        ttk.Separator(main_frm, orient=HORIZONTAL).grid(row=8, column=0, columnspan=4, sticky='ew')

        ttk.Button(main_frm, text= 'Pagar', command=self.pay_win).grid(row=9, column=1)
        ttk.Button(main_frm, text= 'Modificar', command=self.mod_win).grid(row=9, column=2)

        for child in main_frm.winfo_children():
            child.grid_configure(padx=10, pady=10)
        

    def pay_win(self, *args):
        Pay_Win(self.addr_info)
    
    def mod_win(self, *args):
        Mod_Win(self.addr_info)



class Not_Found:
    def __init__(self, parent):
        for child in parent.winfo_children():
            child.destroy()

        main_frm = ttk.Frame(parent, padding=10)
        main_frm.grid( row=0, column=0 )
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        ttk.Label(main_frm, text='Información No Encontrada ').grid( row=1, column=1, sticky=(W, E) )       
        


class Pay_Win:
    def __init__(self, info):
        self.win = Toplevel(root)
        self.win.title('Pagar ')
        self.win.geometry('400x400+300+200')
        [self.id, self.addr, self.cost, self.balance] = info

        main_frm = ttk.Frame(self.win, padding=10)
        main_frm.grid( row=0, column=0 )
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)

        chg_resta_wrapper = (self.win.register(self.chg_resta), '%P')

        ttk.Label(main_frm, text='Información del Pago: ').grid( row=1, column=1, sticky=(W, E) )

        ttk.Label(main_frm, text= 'Dirección : ').grid(row=2, column=1)
        ttk.Label(main_frm, text= self.addr).grid(row=2, column=2)

        ttk.Label(main_frm, text= 'Costo : ').grid(row=3, column=1)
        ttk.Label(main_frm, text= f'${self.cost}').grid(row=3, column=2)

        ttk.Label(main_frm, text= 'Balance : ').grid(row=4, column=1)
        ttk.Label (main_frm, text= f'${self.balance}').grid(row=4, column=2)

        ttk.Label(main_frm, text= 'Pagar : ').grid(row=6, column=1)
        self.amount = StringVar()
        amt_ent = ttk.Entry(main_frm, textvariable=self.amount, width=5, validate='key', validatecommand=chg_resta_wrapper)
        amt_ent.grid(row=6, column=2)
        
        ttk.Label(main_frm, text= 'Nuevo Balance : ').grid(row=7, column=1)
        self.resta = StringVar()
        self.resta_lbl = ttk.Label(main_frm, textvariable=self.resta)
        self.resta_lbl.grid(row=7, column=2)
        self.resta.set(f'${self.balance}')

        ttk.Separator(main_frm, orient=HORIZONTAL).grid(row=8, column=0, columnspan=4, sticky='ew')

        ttk.Button(main_frm, text= 'Aceptar Pago', command=self.accp_pay).grid(row=9, column=1)
        ttk.Button(main_frm, text= 'Cancelar', command=lambda : self.win.destroy()).grid(row=9, column=2)

        for child in main_frm.winfo_children():
            child.grid_configure(padx=10, pady=10)

        amt_ent.focus()
        self.win.bind('<Return>', self.accp_pay)
    

    def accp_pay(self, *args):
        new_win = Toplevel(self.win)
        new_win.title('Confirmar:')
        new_win.geometry('400x300+275+275')

        main_frm = ttk.Frame(new_win, padding=10)
        main_frm.grid( row=0, column=0 )
        new_win.columnconfigure(0, weight=1)
        new_win.rowconfigure(0, weight=1)

        ttk.Label(main_frm, text= 'Favor de confirmar la información:').grid(row=1, column=1)

        ttk.Label(main_frm, text= 'Dirección : ').grid(row=2, column=1)
        ttk.Label(main_frm, text= self.addr).grid(row=2, column=2)

        ttk.Label(main_frm, text= 'Pago : ').grid(row=3, column=1)
        ttk.Label(main_frm, text= f'${self.amount.get()}').grid(row=3, column=2)

        ttk.Label(main_frm, text= 'Balance : ').grid(row=4, column=1)
        ttk.Label(main_frm, text= f'{self.resta.get()}').grid(row=4, column=2)

        ttk.Separator(main_frm, orient=HORIZONTAL).grid(row=5, column=0, columnspan=4, sticky='we')

        cnf_btn = ttk.Button(main_frm, text= 'Confirmar', command=self.pay_addr)
        cnf_btn.grid(row=6, column=1)
        ttk.Button(main_frm, text= 'Cancelar', command= lambda : new_win.destroy()).grid(row=6, column=2)

        for child in main_frm.winfo_children():
            child.grid_configure(padx=10, pady=10)
        
        cnf_btn.focus()
        

    def chg_resta(self, *args):
        try:
            if args[0] != '':
                value = int(args[0])
            else:
                value = 0
            self.resta.set(f'${value + self.balance}')
            return True
        except:
            return False
    
    def pay_addr(self, *args):
        Controllers.deposit_pay((self.id, self.amount.get(), self.resta.get()))
        self.win.destroy()
        Searcher(root, f1)



class Mod_Win:
    def __init__(self, addr):
        print('heyyyya', addr)


root = Tk()
root.title('Fuentes de Anahuac Administrador de Pagos')
root.minsize(800, 600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#root.attributes('-fullscreen', 1)
#Searcher(root)
#new_window = Toplevel(root)
#new_window.geometry('300x200-5+40')
#new_window.destroy()
ntb = ttk.Notebook(root)
f1 = ttk.Frame(ntb)
f2 = ttk.Frame(ntb)

ntb.add(f1, text='Buscar')
ntb.add(f2, text='Info')
ntb.pack(fill='both', expand=True)
Searcher(root, f1)
root.mainloop()


"""# v2
import tkinter as tk
import Controllers

Controllers.folio_search('Real 300')

window = tk.Tk()
window.columnconfigure([0,4], weight=1, minsize=50)
window.rowconfigure([0,3], weight=1, minsize=100)

'''frm_inp = tk.Frame(master=window)
frm_inp.grid(row=1, column=1)'''

lbl_folio = tk.Label(text="Folio: ")
lbl_folio.grid(row=1, column=1)

ent_folio = tk.Entry()
ent_folio.grid(row=1, column=2)

def folio_search():
    print('Searching the file')
    print('The entry class --> ', ent_folio)

btn_search = tk.Button(text="Buscar", command=folio_search)
btn_search.grid(row=2, column=2)

window.mainloop()
"""



""" # v1
import tkinter as tk

window = tk.Tk()

# Frame for label and entry classes > Search
frm_inp = tk.Frame(master=window, width=200, height=100)
frm_inp.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# Frame for search btn > Search
frm_srch = tk.Frame(master=window, width=200, height=100)
frm_srch.pack(fill= tk.BOTH, side=tk.BOTTOM, expand=True)

# Label class > Search
lbl_folio = tk.Label(text='Folio: ', master=frm_inp)
lbl_folio.pack()

# Entry class > Search
ent_folio = tk.Entry(width=25, master=frm_inp)
ent_folio.pack()

# Button class > Search
btn_search = tk.Button(text="Buscar", master=frm_srch)
btn_search.pack()

window.mainloop()
"""