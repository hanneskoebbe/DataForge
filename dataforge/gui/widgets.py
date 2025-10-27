import tkinter as tk


def widgets(self):
    event = ["<MouseWheel>", "<Double-Button-1>", "<Return>"]

    self.canvas.unbind_all(event[0])

    # Vorherige Checkboxen löschen
    for widget in self.scrollable_frame.winfo_children():
        widget.destroy()
    self.widget_data.clear()

    if self.all_data != {}:
        for param, data in self.all_data.items():
            # new row
            row = tk.Frame(
                self.scrollable_frame,
                width=self.canvas.winfo_width())
            row.pack(fill="x", padx=5, pady=2)
            row.bind(event[1], lambda e, p=param: self.edit_data(p))

            # checkbox
            var = tk.BooleanVar(value=data.get("checked", False))
            cb = tk.Checkbutton(row,  variable=var, anchor="w", justify="left")
            cb.pack(side="left")
            cb.bind(event[1], lambda e, p=param: self.edit_data(p))

            # entry for parameter name
            par_name = tk.Entry(row, width=25)
            par_name.insert(0, str(data.get("par_name", param)))
            par_name.pack(side="left", padx=(10, 2), expand='True', fill='x')
            par_name.bind(event[1], lambda e, p=param: self.edit_data(p))
            par_name.bind(event[2], lambda e, p=param: self.on_input(p))
            tol_frame = tk.Frame(row, width=10)
            tol_frame.pack(side="left", padx=(10, 2), expand='True', fill='x')

            # label for lower tolerance
            tol_low_label = tk.Label(tol_frame, text="untere Tol.:")
            tol_low_label.pack(side="left", padx=(10, 2))
            tol_low_label.bind(event[1], lambda e, p=param: self.edit_data(p))

            # entry for lower tolerance
            tol_low = tk.Entry(tol_frame, width=10)
            tol_low.insert(0, str(data["lower tol."][0]))
            tol_low.pack(side="left", padx=(10, 2), expand='True')
            tol_low.bind(event[1], lambda e, p=param: self.edit_data(p))
            tol_low.bind(event[2], lambda e, p=param: self.on_input(p))

            # label for upper tolerance
            tol_up_label = tk.Label(tol_frame, text="obere Tol.:")
            tol_up_label.pack(side="left", padx=(10, 2))
            tol_up_label.bind(event[1], lambda e, p=param: self.edit_data(p))

            # entry for upper tolerance
            tol_up = tk.Entry(tol_frame, width=6)
            tol_up.insert(0, str(data["upper tol."][0]))
            tol_up.pack(side="left", padx=(10, 20), expand='True')
            tol_up.bind(event[1], lambda e, p=param: self.edit_data(p))
            tol_up.bind(event[2], lambda e, p=param: self.on_input(p))

            # delete-button
            remove_btn = tk.Button(
                tol_frame,
                text="✕",
                command=lambda p=param: self.on_remove(p),
                width=2,
                relief='flat',
                bg='white',
                fg='red',
                font=("Arial", 10, "bold"),
                padx=0, pady=0
            )
            remove_btn.pack(side='right', padx=(2, 0))

            # option-button
            options_btn = tk.Button(
                tol_frame,
                text="⋮",  # U+22EE Vertical Ellipsis
                command=lambda p=param: self.on_options(p),
                width=2,
                relief='flat',
                bg='white',
                fg='black',
                font=("Arial", 10),
                padx=0, pady=0
            )
            options_btn.pack(side='right', padx=(0, 2))

            # save data in self.widget_data
            self.widget_data[param] = {
                "var": var,
                "par_name": par_name,
                "tol_low": tol_low,
                "tol_up": tol_up
            }
        self.canvas.bind_all(event[0], self.on_mousewheel)
