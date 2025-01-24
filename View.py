import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
from Controller import CourseController

class CourseView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Cours")
        self.controller = CourseController()

        # Remove the default title bar
        self.root.overrideredirect(True)  # This removes the title bar

        # Set the main window background color
        self.root.configure(bg='#3f4738')

        # Create a custom title bar
        self.create_custom_title_bar()

        # Create a main container for the rest of the application
        self.main_container = tk.Frame(self.root, bg='#3f4738')
        self.main_container.pack(fill=tk.BOTH, expand=True)  # Use pack for the main container

        # Apply a custom theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic'

        # Configure colors and fonts
        self.style.configure('.', background='#3f4738', foreground='white', font=('Arial', 10))
        self.style.configure('TLabel', background='#3f4738', foreground='white')
        self.style.configure('TButton', background='#4c5844', foreground='white', borderwidth=1)
        self.style.map('TButton', background=[('active', '#968732')])
        self.style.configure('TEntry', fieldbackground='#4c5844', foreground='white')
        self.style.configure('Treeview', background='#4c5844', fieldbackground='#4c5844', foreground='white')
        self.style.map('Treeview', background=[('selected', '#968732')])
        self.style.configure('Treeview.Heading', background='#3f4738', foreground='white')
        self.style.configure('TLabelframe', background='#3f4738', foreground='white')
        self.style.configure('TLabelframe.Label', background='#3f4738', foreground='white')

        # creer le form
        self.create_form()
        # creer les buttons
        self.create_buttons()
        # creer la list de display
        self.create_grid()
        # creer status bar
        self.create_status_bar()

        #  keyboard shortcuts
        self.root.bind("<Return>", lambda event: self.ajouter_cours())  # Enter key for Ajouter
        self.root.bind("<Delete>", lambda event: self.supprimer_cours())  # Delete key for Supprimer
        self.root.bind("<space>", lambda event: self.consulter_cours())  # Space key for Consulter

    def create_custom_title_bar(self):
        # Create a custom title bar frame
        title_bar = tk.Frame(self.root, bg='#3f4738', relief='raised', bd=0)
        title_bar.pack(fill=tk.X)  # Use pack for the title bar

        # Add a title label
        title_label = tk.Label(title_bar, text="Gestion des Cours by Valve", bg='#3f4738', fg='white', font=('Arial', 10))
        title_label.pack(side=tk.LEFT, padx=10)

        # Add close button
        close_button = tk.Button(title_bar, text="X", bg='#3f4738', fg='white', bd=0, command=self.root.destroy)
        close_button.pack(side=tk.RIGHT, padx=10)

        # Add minimize button
        minimize_button = tk.Button(title_bar, text="-", bg='#3f4738', fg='white', bd=0, command=self.minimize_window)
        minimize_button.pack(side=tk.RIGHT, padx=10)

        # Bind mouse events to allow dragging the window
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.on_move)

    def minimize_window(self):
        # Minimize the window by withdrawing it and then re-displaying it as an icon
        self.root.withdraw()  # Hide the window
        self.root.update_idletasks()
        self.root.iconify()  # Minimize the window

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def create_form(self):
        # Create a frame for the form
        form_frame = ttk.LabelFrame(self.main_container, text="Formulaire de Cours", padding=(10, 5))
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Use grid for the form

        # Create labels and entry fields
        labels = ["Titre", "Description", "Categorie", "Niveau", 
                 "Duree", "Instructeur", "Date de publication"]
        
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(form_frame, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[label] = entry

        # Add image to the right of the form fields
        self.add_image(form_frame)  # Pass the form_frame as the parent

    def add_image(self, parent_frame):
        # Load the image using Pillow
        try:
            image_path = "images/cours.jpg"  # Replace with the path to your image
            self.image = Image.open(image_path)
            # Resize the image 
            self.image = self.image.resize((400, 250), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)

            # Create a label to display the image
            image_label = ttk.Label(parent_frame, image=self.tk_image)
            image_label.grid(row=0, column=2, rowspan=len(self.entries), padx=10, pady=10, sticky="nsew")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")

    def create_buttons(self):
        buttons_frame = ttk.Frame(self.main_container)
        buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # Use grid for buttons

        button_style = {'width': 10, 'padding': 5}
        ttk.Button(buttons_frame, text="Ajouter", command=self.ajouter_cours).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Modifier", command=self.modifier_cours).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Supprimer", command=self.supprimer_cours).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Consulter", command=self.consulter_cours).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Rechercher", command=self.rechercher_cours).pack(side=tk.LEFT, padx=5)

    def create_grid(self):
      grid_frame = ttk.LabelFrame(self.main_container, text="Liste des Cours", padding=(10, 5))
      grid_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")  # Use grid for the Treeview

      # Create Treeview
      columns = ("ID", "Titre", "Description", "Categorie", "Niveau", "Duree", "Instructeur", "Date")
      self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings", height=10)
    
      # Configure column widths
      widths = [50, 100, 200, 100, 80, 60, 100, 100]
      for col, width in zip(columns, widths):
          self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))  # Add click event
          self.tree.column(col, width=width)

      # Add scrollbars
      yscroll = ttk.Scrollbar(grid_frame, orient=tk.VERTICAL, command=self.tree.yview)
      xscroll = ttk.Scrollbar(grid_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
      self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

      # Grid layout
      self.tree.grid(row=0, column=0, sticky="nsew")
      yscroll.grid(row=0, column=1, sticky="ns")
      xscroll.grid(row=1, column=0, sticky="ew")

    def sort_treeview(self, col):
      # Get all items from the Treeview
      items = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
     
  # Sort items based on the column values
      items.sort()
    
      # Reinsert sorted items into the Treeview
      for index, (val, child) in enumerate(items):
          self.tree.move(child, '', index)
    
    # Reverse the order if the column is already sorted
      if self.tree.heading(col)['text'] == col + ' ▲':
          items.reverse()
          for index, (val, child) in enumerate(items):
              self.tree.move(child, '', index)
          self.tree.heading(col, text=col + ' ▼')
      else:
          self.tree.heading(col, text=col + ' ▲')

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.main_container, text="Pret", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky="ew", padx=10, pady=10)  # Use grid for the status bar

    def update_status(self, message):
        self.status_bar.config(text=message)

    def get_form_data(self):
        return tuple(entry.get() for entry in self.entries.values())

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def ajouter_cours(self):
        data = self.get_form_data()
        if all(data):
            self.controller.ajouter_cours(data)
            messagebox.showinfo("Succes", "Cours ajoute avec succes!")
            self.clear_form()
            self.consulter_cours()
            self.update_status("Cours ajoute avec succes!")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs!")
            self.update_status("Erreur: Veuillez remplir tous les champs!")

    def modifier_cours(self):
        selected = self.tree.selection()
        if selected:
            data = self.get_form_data()
            if all(data):
                course_id = self.tree.item(selected[0])['values'][0]
                self.controller.modifier_cours(course_id, data)
                messagebox.showinfo("Succes", "Cours modifie avec succes!")
                self.clear_form()
                self.consulter_cours()
                self.update_status("Cours modifie avec succes!")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs!")
                self.update_status("Erreur: Veuillez remplir tous les champs!")
        else:
            messagebox.showerror("Erreur", "Veuillez selectionner un cours a modifier!")
            self.update_status("Erreur: Veuillez selectionner un cours a modifier!")

    def supprimer_cours(self):
        selected = self.tree.selection()
        if selected:
            course_id = self.tree.item(selected[0])['values'][0]
            self.controller.supprimer_cours(course_id)
            messagebox.showinfo("Succes", "Cours supprime avec succes!")
            self.consulter_cours()
            self.update_status("Cours supprime avec succes!")
        else:
            messagebox.showerror("Erreur", "Veuillez selectionner un cours a supprimer!")
            self.update_status("Erreur: Veuillez selectionner un cours a supprimer!")

    def consulter_cours(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        courses = self.controller.consulter_cours()
        for course in courses:
            self.tree.insert("", tk.END, values=course)
        self.update_status("Liste des cours mise a jour.")

    def rechercher_cours(self):
        titre = self.entries["Titre"].get()
        if titre:
            for item in self.tree.get_children():
                self.tree.delete(item)
            courses = self.controller.rechercher_cours(titre)
            for course in courses:
                self.tree.insert("", tk.END, values=course)
            self.update_status(f"Recherche effectuee pour: {titre}")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un titre a rechercher!")
            self.update_status("Erreur: Veuillez entrer un titre a rechercher!")

