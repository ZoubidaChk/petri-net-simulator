"""
SIMULATEUR DE RÉSEAU DE PETRI 
Made by Zoubida Rawan 

Interface graphique avec visualisation!
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math

class PetriNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" Simulateur de Réseau de Petri - By Zoubida Rawan ")
        self.root.geometry("1400x800")
        self.root.configure(bg="#FFE4E9")
        
        # Données du réseau
        self.places = {}  # {id: {'name': str, 'tokens': int, 'x': float, 'y': float}}
        self.transitions = {}  # {id: {'name': str, 'x': float, 'y': float}}
        self.arcs = []  # [{'from': id, 'to': id, 'weight': int}]
        
        self.place_counter = 0
        self.trans_counter = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface"""
        # Header
        header = tk.Frame(self.root, bg="#EED5E2", height=80)
        header.pack(fill=tk.X, pady=(0, 10))
        
        title = tk.Label(header, text=" SIMULATEUR DE RÉSEAU DE PETRI", 
                        font=("Arial", 20, "bold"), bg="#ECDBE4", fg="white")
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text="Made by Zoubida Rawan 🌸", 
                           font=("Arial", 12), bg="#9BC2EE", fg="#FFE4E9")
        subtitle.pack()
        
        # Conteneur principal
        main_container = tk.Frame(self.root, bg="#FFE4E9")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panneau gauche (contrôles)
        left_panel = tk.Frame(main_container, bg="#FFF0F5", width=350, relief=tk.RAISED, bd=3)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.setup_controls(left_panel)
        
        # Canvas central (visualisation)
        canvas_frame = tk.Frame(main_container, bg="white", relief=tk.SUNKEN, bd=3)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#FFF5F7", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Panneau droit (état)
        right_panel = tk.Frame(main_container, bg="#FFF0F5", width=250, relief=tk.RAISED, bd=3)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        self.setup_state_panel(right_panel)
        
    def setup_controls(self, parent):
        """Configure les contrôles"""
        # Section Places
        place_frame = tk.LabelFrame(parent, text=" CRÉER UNE PLACE", 
                                   font=("Arial", 11, "bold"),
                                   bg="#FFE4F0", fg="#EBE4E8", bd=2)
        place_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(place_frame, text="Nom:", bg="#FFE4F0", font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(5,0))
        self.place_name_entry = tk.Entry(place_frame, font=("Arial", 10), bg="white")
        self.place_name_entry.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(place_frame, text="Jetons:", bg="#FFE4F0", font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(5,0))
        self.place_tokens_entry = tk.Entry(place_frame, font=("Arial", 10), bg="white")
        self.place_tokens_entry.insert(0, "0")
        self.place_tokens_entry.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Button(place_frame, text="✨ Ajouter Place", command=self.add_place,
                 bg="#FF69B4", fg="white", font=("Arial", 10, "bold"),
                 activebackground="#FF1493", cursor="hand2").pack(pady=10, padx=5, fill=tk.X)
        
        # Section Transitions
        trans_frame = tk.LabelFrame(parent, text="✨ CRÉER UNE TRANSITION", 
                                   font=("Arial", 11, "bold"),
                                   bg="#E6F7FF", fg="#1E90FF", bd=2)
        trans_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(trans_frame, text="Nom:", bg="#E6F7FF", font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(5,0))
        self.trans_name_entry = tk.Entry(trans_frame, font=("Arial", 10), bg="white")
        self.trans_name_entry.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Button(trans_frame, text="💫 Ajouter Transition", command=self.add_transition,
                 bg="#87CEEB", fg="white", font=("Arial", 10, "bold"),
                 activebackground="#4682B4", cursor="hand2").pack(pady=10, padx=5, fill=tk.X)
        
        # Section Arcs
        arc_frame = tk.LabelFrame(parent, text="💝 CRÉER UN ARC", 
                                 font=("Arial", 11, "bold"),
                                 bg="#F0E6FF", fg="#8B008B", bd=2)
        arc_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(arc_frame, text="Depuis:", bg="#F0E6FF", font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(5,0))
        self.arc_from_combo = ttk.Combobox(arc_frame, font=("Arial", 9), state="readonly")
        self.arc_from_combo.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(arc_frame, text="Vers:", bg="#F0E6FF", font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(5,0))
        self.arc_to_combo = ttk.Combobox(arc_frame, font=("Arial", 9), state="readonly")
        self.arc_to_combo.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(arc_frame, text="Poids:", bg="#F0E6FF", font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(5,0))
        self.arc_weight_entry = tk.Entry(arc_frame, font=("Arial", 10), bg="white")
        self.arc_weight_entry.insert(0, "1")
        self.arc_weight_entry.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Button(arc_frame, text="💖 Créer Arc", command=self.add_arc,
                 bg="#DA70D6", fg="white", font=("Arial", 10, "bold"),
                 activebackground="#BA55D3", cursor="hand2").pack(pady=10, padx=5, fill=tk.X)
        
        # Boutons actions
        action_frame = tk.Frame(parent, bg="#FFF0F5")
        action_frame.pack(fill=tk.X, padx=10, pady=20)
        
        tk.Button(action_frame, text="📚 Charger Exemple", command=self.load_example,
                 bg="#98FB98", fg="black", font=("Arial", 9, "bold"),
                 cursor="hand2").pack(fill=tk.X, pady=3)
        
        tk.Button(action_frame, text="🔄 Réinitialiser", command=self.reset,
                 bg="#FFB6C1", fg="black", font=("Arial", 9, "bold"),
                 cursor="hand2").pack(fill=tk.X, pady=3)
        
    def setup_state_panel(self, parent):
        """Configure le panneau d'état"""
        tk.Label(parent, text="💖 ÉTAT DU RÉSEAU", font=("Arial", 12, "bold"),
                bg="#FFF0F5", fg="#C71585").pack(pady=10)
        
        # Liste des places
        tk.Label(parent, text="🌸 Places:", font=("Arial", 10, "bold"),
                bg="#FFF0F5", fg="#FF69B4").pack(anchor=tk.W, padx=10, pady=(10,5))
        
        places_frame = tk.Frame(parent, bg="white", relief=tk.SUNKEN, bd=2)
        places_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.places_listbox = tk.Listbox(places_frame, font=("Arial", 9), 
                                         bg="white", fg="#C71585", bd=0)
        self.places_listbox.pack(fill=tk.BOTH, expand=True)
        self.places_listbox.bind('<Double-Button-1>', self.modify_tokens)
        
        # Liste des transitions
        tk.Label(parent, text="✨ Transitions:", font=("Arial", 10, "bold"),
                bg="#FFF0F5", fg="#1E90FF").pack(anchor=tk.W, padx=10, pady=(10,5))
        
        trans_frame = tk.Frame(parent, bg="white", relief=tk.SUNKEN, bd=2)
        trans_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.trans_listbox = tk.Listbox(trans_frame, font=("Arial", 9),
                                        bg="white", fg="#1E90FF", bd=0)
        self.trans_listbox.pack(fill=tk.BOTH, expand=True)
        self.trans_listbox.bind('<Double-Button-1>', self.fire_transition)
        
        tk.Label(parent, text="💡 Double-cliquez pour franchir!", 
                font=("Arial", 8, "italic"), bg="#FFF0F5", fg="#666").pack(pady=5)
        
    def add_place(self):
        """Ajoute une place"""
        name = self.place_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Attention", "💕 Entrez un nom pour la place!")
            return
        
        try:
            tokens = int(self.place_tokens_entry.get())
        except:
            tokens = 0
        
        place_id = f"p{self.place_counter}"
        self.place_counter += 1
        
        # Position aléatoire
        x = 100 + (self.place_counter % 5) * 150
        y = 100 + (self.place_counter // 5) * 120
        
        self.places[place_id] = {
            'name': name,
            'tokens': tokens,
            'x': x,
            'y': y
        }
        
        self.place_name_entry.delete(0, tk.END)
        self.place_tokens_entry.delete(0, tk.END)
        self.place_tokens_entry.insert(0, "0")
        
        self.update_display()
        messagebox.showinfo("Succès", f"✨ Place '{name}' créée avec {tokens} jeton(s)!")
        
    def add_transition(self):
        """Ajoute une transition"""
        name = self.trans_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Attention", "💕 Entrez un nom pour la transition!")
            return
        
        trans_id = f"t{self.trans_counter}"
        self.trans_counter += 1
        
        x = 100 + (self.trans_counter % 5) * 150
        y = 300 + (self.trans_counter // 5) * 120
        
        self.transitions[trans_id] = {
            'name': name,
            'x': x,
            'y': y
        }
        
        self.trans_name_entry.delete(0, tk.END)
        
        self.update_display()
       
    def add_arc(self):
        """Ajoute un arc"""
        from_id = self.arc_from_combo.get().split(':')[0] if self.arc_from_combo.get() else None
        to_id = self.arc_to_combo.get().split(':')[0] if self.arc_to_combo.get() else None
        
        if not from_id or not to_id:
            messagebox.showwarning("Attention", "💕 Sélectionnez le départ et l'arrivée!")
            return
        
        try:
            weight = int(self.arc_weight_entry.get())
        except:
            weight = 1
        
        # Vérifier que c'est place->transition ou transition->place
        from_is_place = from_id.startswith('p')
        to_is_place = to_id.startswith('p')
        
        if from_is_place == to_is_place:
            messagebox.showerror("Erreur", "💔 Un arc doit connecter une place à une transition!")
            return
        
        self.arcs.append({
            'from': from_id,
            'to': to_id,
            'weight': weight
        })
        
        self.update_display()
      
    def is_enabled(self, trans_id):
        """Vérifie si une transition est franchissable"""
        for arc in self.arcs:
            if arc['to'] == trans_id and arc['from'].startswith('p'):
                place = self.places[arc['from']]
                if place['tokens'] < arc['weight']:
                    return False
        return True
        
    def fire_transition(self, event=None):
        """Franchit une transition"""
        selection = self.trans_listbox.curselection()
        if not selection:
            return
        
        trans_text = self.trans_listbox.get(selection[0])
        trans_id = trans_text.split(':')[0]
        
        if not self.is_enabled(trans_id):
            messagebox.showwarning("Impossible", "🚫 Cette transition n'est pas franchissable!")
            return
        
        # Retirer jetons
        for arc in self.arcs:
            if arc['to'] == trans_id and arc['from'].startswith('p'):
                self.places[arc['from']]['tokens'] -= arc['weight']
        
        # Ajouter jetons
        for arc in self.arcs:
            if arc['from'] == trans_id and arc['to'].startswith('p'):
                self.places[arc['to']]['tokens'] += arc['weight']
        
        self.update_display()
        
    def modify_tokens(self, event=None):
        """Modifie les jetons d'une place"""
        selection = self.places_listbox.curselection()
        if not selection:
            return
        
        place_text = self.places_listbox.get(selection[0])
        place_id = place_text.split(':')[0]
        place = self.places[place_id]
        
        new_tokens = simpledialog.askinteger("Modifier jetons",
                                            f"Nouveaux jetons pour {place['name']}:",
                                            initialvalue=place['tokens'],
                                            minvalue=0)
        
        if new_tokens is not None:
            place['tokens'] = new_tokens
            self.update_display()
        
    def update_display(self):
        """Met à jour l'affichage"""
        self.canvas.delete("all")
        
        # Dessiner les arcs
        for arc in self.arcs:
            from_node = self.places.get(arc['from']) or self.transitions.get(arc['from'])
            to_node = self.places.get(arc['to']) or self.transitions.get(arc['to'])
            
            if from_node and to_node:
                self.canvas.create_line(from_node['x'], from_node['y'],
                                      to_node['x'], to_node['y'],
                                      arrow=tk.LAST, fill="#FF69B4", width=3)
                
                if arc['weight'] > 1:
                    mx = (from_node['x'] + to_node['x']) / 2
                    my = (from_node['y'] + to_node['y']) / 2
                    self.canvas.create_text(mx, my - 10, text=str(arc['weight']),
                                          font=("Arial", 12, "bold"), fill="#C71585")
        
        # Dessiner les places
        for place_id, place in self.places.items():
            x, y = place['x'], place['y']
            
            # Cercle
            self.canvas.create_oval(x-30, y-30, x+30, y+30,
                                  fill="#FFE4F0", outline="#FF69B4", width=3)
            
            # Nom
            self.canvas.create_text(x, y-45, text=place['name'],
                                  font=("Arial", 11, "bold"), fill="#C71585")
            
            # Jetons
            tokens = place['tokens']
            if tokens > 0 and tokens <= 5:
                for i in range(tokens):
                    angle = (i * 2 * math.pi) / tokens
                    radius = 15 if tokens > 1 else 0
                    tx = x + radius * math.cos(angle)
                    ty = y + radius * math.sin(angle)
                    self.canvas.create_oval(tx-5, ty-5, tx+5, ty+5, fill="#FF1493")
            elif tokens > 5:
                self.canvas.create_text(x, y, text=str(tokens),
                                      font=("Arial", 16, "bold"), fill="#FF1493")
        
        # Dessiner les transitions
        for trans_id, trans in self.transitions.items():
            x, y = trans['x'], trans['y']
            
            enabled = self.is_enabled(trans_id)
            color = "#90EE90" if enabled else "#D3D3D3"
            
            # Rectangle
            self.canvas.create_rectangle(x-25, y-35, x+25, y+35,
                                        fill=color, outline="#228B22" if enabled else "#808080",
                                        width=3)
            
            # Nom
            self.canvas.create_text(x, y-50, text=trans['name'],
                                  font=("Arial", 11, "bold"),
                                  fill="#228B22" if enabled else "#808080")
        
        # Mettre à jour les comboboxes
        place_items = [f"{pid}: {p['name']}" for pid, p in self.places.items()]
        trans_items = [f"{tid}: {t['name']}" for tid, t in self.transitions.items()]
        
        self.arc_from_combo['values'] = place_items + trans_items
        self.arc_to_combo['values'] = place_items + trans_items
        
        # Mettre à jour les listbox
        self.places_listbox.delete(0, tk.END)
        for pid, p in self.places.items():
            self.places_listbox.insert(tk.END, f"{pid}: {p['name']} ({'💖'*min(p['tokens'],5) if p['tokens']<=5 else str(p['tokens'])+'💖'})")
        
        self.trans_listbox.delete(0, tk.END)
        for tid, t in self.transitions.items():
            enabled = "💚 Franchissable" if self.is_enabled(tid) else "🚫 Bloquée"
            self.trans_listbox.insert(tk.END, f"{tid}: {t['name']} - {enabled}")
    
    def load_example(self):
        """Charge un exemple"""
        self.reset_silent()
        
        # Créer un exemple simple
        self.places['p0'] = {'name': 'P1', 'tokens': 2, 'x': 200, 'y': 150}
        self.places['p1'] = {'name': 'P2', 'tokens': 0, 'x': 500, 'y': 150}
        self.places['p2'] = {'name': 'P3', 'tokens': 1, 'x': 350, 'y': 280}
        
        self.transitions['t0'] = {'name': 'T1', 'x': 350, 'y': 150}
        
        self.arcs = [
            {'from': 'p0', 'to': 't0', 'weight': 1},
            {'from': 't0', 'to': 'p1', 'weight': 1},
            {'from': 'p2', 'to': 't0', 'weight': 1}
        ]
        
        self.place_counter = 3
        self.trans_counter = 1
        
        self.update_display()
        messagebox.showinfo("Exemple", "📚 Exemple chargé! Double-cliquez sur T1 pour la franchir!")
    
    def reset_silent(self):
        """Réinitialise sans message"""
        self.places.clear()
        self.transitions.clear()
        self.arcs.clear()
        self.place_counter = 0
        self.trans_counter = 0
        self.update_display()
    
    def reset(self):
        """Réinitialise le réseau"""
        if messagebox.askyesno("Confirmer", "💔 Voulez-vous vraiment tout réinitialiser?"):
            self.reset_silent()
            messagebox.showinfo("Réinitialisation", "✨ Réseau réinitialisé!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PetriNetGUI(root)
    root.mainloop()
