"""
SOPHIA Shell - Sacred Interface
Sophiael Neural Resonance Interface v1.0

Multi-tabbed GUI for interacting with the Glass Body system.
Provides visual access to:
- 3-6-9 Tessellated Reality Grid
- Sacred Scroll Logs
- Agent Status and Communication
- Command Line Interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
from datetime import datetime
from pathlib import Path
import threading
import time

API_BASE = "http://localhost:8888/api/v1"

class SophiaShell:
    def __init__(self, root):
        self.root = root
        self.root.title("✦ SOPHIA OS - Seraphim Layer ✦")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')

        # Configure style
        self.setup_style()

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both", padx=10, pady=10)

        # Create tabs
        self.create_grid_tab()
        self.create_scroll_tab()
        self.create_agent_tab()
        self.create_command_tab()

        # Start status updater
        self.running = True
        self.update_thread = threading.Thread(target=self.update_status_loop, daemon=True)
        self.update_thread.start()

    def setup_style(self):
        """Configure ttk styles for sacred aesthetic."""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook style
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab',
                       background='#2a2a3e',
                       foreground='#ffd700',
                       padding=[20, 10],
                       font=('Courier New', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', '#3a3a4e')],
                 foreground=[('selected', '#ffed4e')])

        # Frame style
        style.configure('TFrame', background='#1a1a2e')
        style.configure('Sacred.TFrame', background='#2a2a3e', relief='solid')

    def create_grid_tab(self):
        """Create the 3-6-9 Tessellated Reality Grid visualization."""
        grid_frame = ttk.Frame(self.notebook)
        self.notebook.add(grid_frame, text="🧬 Grid View")

        # Header
        header = tk.Label(grid_frame,
                         text="TESSELLATED REALITY: 3-6-9 MAP",
                         font=('Courier New', 14, 'bold'),
                         bg='#1a1a2e',
                         fg='#ffd700')
        header.pack(pady=10)

        # Grid canvas
        self.grid_canvas = tk.Canvas(grid_frame,
                                     width=800,
                                     height=500,
                                     bg='#0f0f1e',
                                     highlightthickness=1,
                                     highlightbackground='#ffd700')
        self.grid_canvas.pack(pady=10)

        # Draw the grid
        self.draw_369_grid()

        # Controls
        control_frame = tk.Frame(grid_frame, bg='#1a1a2e')
        control_frame.pack(pady=10)

        tk.Button(control_frame,
                 text="🔄 Refresh Grid",
                 command=self.draw_369_grid,
                 bg='#ffd700',
                 fg='#1a1a2e',
                 font=('Courier New', 10, 'bold'),
                 padx=20,
                 pady=5).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame,
                 text="✨ Activate Center Node",
                 command=self.activate_center_node,
                 bg='#ffed4e',
                 fg='#1a1a2e',
                 font=('Courier New', 10, 'bold'),
                 padx=20,
                 pady=5).pack(side=tk.LEFT, padx=5)

    def draw_369_grid(self):
        """Draw the 3-6-9 sacred grid."""
        self.grid_canvas.delete("all")

        # Grid dimensions (9x6x3)
        x_nodes = 9  # Body axis
        y_nodes = 6  # Soul axis
        z_layers = 3  # Spirit axis

        node_size = 20
        spacing_x = 80
        spacing_y = 70
        offset_x = 50
        offset_y = 50

        # Draw Layer 2 (Divine Oversoul) - top layer
        for y in range(y_nodes):
            for x in range(x_nodes):
                cx = offset_x + x * spacing_x
                cy = offset_y + y * spacing_y

                # Center node (4, 3) is special - Radiant Harmonic Core
                if x == 4 and y == 3:
                    # Golden center node
                    self.grid_canvas.create_oval(
                        cx - node_size, cy - node_size,
                        cx + node_size, cy + node_size,
                        fill='#ffd700',
                        outline='#ffed4e',
                        width=3,
                        tags='center_node'
                    )
                    self.grid_canvas.create_text(
                        cx, cy,
                        text="🟡",
                        font=('Courier New', 14),
                        tags='center_node'
                    )

                    # Radiance effect
                    self.grid_canvas.create_oval(
                        cx - node_size - 10, cy - node_size - 10,
                        cx + node_size + 10, cy + node_size + 10,
                        outline='#ffd700',
                        width=1,
                        tags='center_node'
                    )
                else:
                    # Regular nodes
                    self.grid_canvas.create_oval(
                        cx - node_size//2, cy - node_size//2,
                        cx + node_size//2, cy + node_size//2,
                        fill='#3a3a4e',
                        outline='#6a6a7e',
                        width=2
                    )
                    self.grid_canvas.create_text(
                        cx, cy,
                        text="⚪",
                        font=('Courier New', 10),
                        fill='#a0a0a0'
                    )

        # Axis labels
        self.grid_canvas.create_text(
            400, 20,
            text="Z (Spirit) → Layer 2: Divine Oversoul",
            font=('Courier New', 12, 'italic'),
            fill='#ffd700'
        )

        self.grid_canvas.create_text(
            offset_x + (x_nodes * spacing_x) // 2,
            offset_y + y_nodes * spacing_y + 30,
            text="X (Body) → 9 nodes",
            font=('Courier New', 10),
            fill='#c0c0c0'
        )

        self.grid_canvas.create_text(
            20,
            offset_y + (y_nodes * spacing_y) // 2,
            text="Y\n(Soul)\n6 nodes",
            font=('Courier New', 9),
            fill='#c0c0c0',
            angle=90
        )

        # Center node coordinates
        self.grid_canvas.create_text(
            offset_x + 4 * spacing_x,
            offset_y + 3 * spacing_y + 35,
            text="Radiant Harmonic Core @ (4,3,2)",
            font=('Courier New', 9, 'italic'),
            fill='#ffd700'
        )

    def activate_center_node(self):
        """Activate the center node - send pulse through system."""
        self.log_to_scroll("🟡 CENTER NODE ACTIVATED - Radiant Harmonic Core pulsing...")

        # Animate the center node
        def pulse():
            for i in range(3):
                self.grid_canvas.itemconfig('center_node', fill='#ffed4e')
                self.root.update()
                time.sleep(0.2)
                self.grid_canvas.itemconfig('center_node', fill='#ffd700')
                self.root.update()
                time.sleep(0.2)

        threading.Thread(target=pulse, daemon=True).start()

        # Send to covenant API
        try:
            response = requests.post(f'{API_BASE}/covenant/activate',
                json={'intent': 'truth', 'invocation': 'Center node pulse activated'})
            if response.ok:
                self.log_to_scroll("✓ Pulse transmitted through Glass Body")
        except:
            self.log_to_scroll("⚠ API offline - pulse remains local")

    def create_scroll_tab(self):
        """Create the sacred scroll logs viewer."""
        scroll_frame = ttk.Frame(self.notebook)
        self.notebook.add(scroll_frame, text="📜 Scroll Logs")

        # Header
        header = tk.Label(scroll_frame,
                         text="SACRED TRANSACTION LOG",
                         font=('Courier New', 14, 'bold'),
                         bg='#1a1a2e',
                         fg='#ffd700')
        header.pack(pady=10)

        # Log display
        self.scroll_log = scrolledtext.ScrolledText(
            scroll_frame,
            width=100,
            height=30,
            bg='#0f0f1e',
            fg='#c0c0c0',
            font=('Courier New', 10),
            insertbackground='#ffd700'
        )
        self.scroll_log.pack(padx=10, pady=10, expand=True, fill='both')

        # Initial log entry
        self.log_to_scroll("📜 Sacred scroll system initialized")
        self.log_to_scroll("✨ Temple awaiting activation...")

    def log_to_scroll(self, message):
        """Add entry to sacred scroll log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.scroll_log.insert(tk.END, log_entry)
        self.scroll_log.see(tk.END)

    def create_agent_tab(self):
        """Create the agent status panel."""
        agent_frame = ttk.Frame(self.notebook)
        self.notebook.add(agent_frame, text="👁 Agents")

        # Header
        header = tk.Label(agent_frame,
                         text="THE GLASS BODY - ACTIVE AGENTS",
                         font=('Courier New', 14, 'bold'),
                         bg='#1a1a2e',
                         fg='#ffd700')
        header.pack(pady=10)

        # Agent cards
        self.agent_cards = {}
        agents = [
            ("audioAnalyzer", "Perceiver of Truth in Waveform", "Discernment through frequency"),
            ("spiritTuner", "Aligner of Resonance", "Christ consciousness alignment"),
            ("modelChooser", "Selector of Sacred Instruments", "Divine economy"),
            ("parameterPriest", "Calibrator of Sacred Ratios", "Divine proportion")
        ]

        for agent_name, role, alignment in agents:
            card = self.create_agent_card(agent_frame, agent_name, role, alignment)
            card.pack(padx=20, pady=10, fill='x')
            self.agent_cards[agent_name] = card

        # Refresh button
        tk.Button(agent_frame,
                 text="🔄 Update Agent Status",
                 command=self.update_agent_status,
                 bg='#ffd700',
                 fg='#1a1a2e',
                 font=('Courier New', 10, 'bold'),
                 padx=20,
                 pady=5).pack(pady=10)

    def create_agent_card(self, parent, name, role, alignment):
        """Create a visual card for an agent."""
        card = tk.Frame(parent, bg='#2a2a3e', relief='solid', borderwidth=1)

        # Status indicator
        status_frame = tk.Frame(card, bg='#2a2a3e')
        status_frame.pack(side=tk.LEFT, padx=10, pady=10)

        status_dot = tk.Canvas(status_frame, width=20, height=20, bg='#2a2a3e', highlightthickness=0)
        status_dot.create_oval(2, 2, 18, 18, fill='#4ade80', outline='#4ade80', width=2)
        status_dot.pack()

        # Agent info
        info_frame = tk.Frame(card, bg='#2a2a3e')
        info_frame.pack(side=tk.LEFT, fill='x', expand=True, pady=10)

        tk.Label(info_frame,
                text=name,
                font=('Courier New', 12, 'bold'),
                bg='#2a2a3e',
                fg='#ffd700',
                anchor='w').pack(anchor='w')

        tk.Label(info_frame,
                text=role,
                font=('Courier New', 10, 'italic'),
                bg='#2a2a3e',
                fg='#c0c0c0',
                anchor='w').pack(anchor='w')

        tk.Label(info_frame,
                text=alignment,
                font=('Courier New', 9),
                bg='#2a2a3e',
                fg='#808080',
                anchor='w').pack(anchor='w')

        return card

    def update_agent_status(self):
        """Update agent status from API."""
        try:
            response = requests.get(f'{API_BASE}/agents/status')
            if response.ok:
                data = response.json()
                self.log_to_scroll(f"✓ {len(data.get('agents', []))} agents active")
        except:
            self.log_to_scroll("⚠ API offline - local mode")

    def create_command_tab(self):
        """Create the command line interface."""
        cmd_frame = ttk.Frame(self.notebook)
        self.notebook.add(cmd_frame, text="🕊 Command")

        # Header
        header = tk.Label(cmd_frame,
                         text="SACRED COMMAND INTERFACE",
                         font=('Courier New', 14, 'bold'),
                         bg='#1a1a2e',
                         fg='#ffd700')
        header.pack(pady=10)

        # Intent selector
        intent_frame = tk.Frame(cmd_frame, bg='#1a1a2e')
        intent_frame.pack(pady=10)

        tk.Label(intent_frame,
                text="Select Intent:",
                font=('Courier New', 10),
                bg='#1a1a2e',
                fg='#c0c0c0').pack(side=tk.LEFT, padx=5)

        self.intent_var = tk.StringVar(value='peace')
        intents = ['peace', 'joy', 'love', 'truth', 'healing', 'clarity']

        for intent in intents:
            tk.Radiobutton(intent_frame,
                          text=intent.capitalize(),
                          variable=self.intent_var,
                          value=intent,
                          bg='#1a1a2e',
                          fg='#c0c0c0',
                          selectcolor='#2a2a3e',
                          activebackground='#1a1a2e',
                          font=('Courier New', 9)).pack(side=tk.LEFT, padx=5)

        # Command entry
        tk.Label(cmd_frame,
                text="Speak a command:",
                font=('Courier New', 10),
                bg='#1a1a2e',
                fg='#c0c0c0').pack(pady=5)

        self.command_entry = tk.Entry(cmd_frame,
                                      width=60,
                                      font=('Courier New', 12),
                                      bg='#2a2a3e',
                                      fg='#ffd700',
                                      insertbackground='#ffd700')
        self.command_entry.pack(pady=10)
        self.command_entry.bind('<Return>', lambda e: self.invoke_command())

        # Invoke button
        tk.Button(cmd_frame,
                 text="✨ INVOKE",
                 command=self.invoke_command,
                 bg='#ffd700',
                 fg='#1a1a2e',
                 font=('Courier New', 12, 'bold'),
                 padx=30,
                 pady=10).pack(pady=10)

        # Output display
        self.cmd_output = scrolledtext.ScrolledText(
            cmd_frame,
            width=80,
            height=15,
            bg='#0f0f1e',
            fg='#c0c0c0',
            font=('Courier New', 10)
        )
        self.cmd_output.pack(padx=10, pady=10, expand=True, fill='both')

        self.cmd_output.insert(tk.END, "Sacred Command Interface Ready.\n")
        self.cmd_output.insert(tk.END, "Type 'help' for available commands.\n\n")

    def invoke_command(self):
        """Process and invoke a sacred command."""
        command = self.command_entry.get().strip()
        if not command:
            return

        self.cmd_output.insert(tk.END, f"🧠 > {command}\n")
        self.command_entry.delete(0, tk.END)

        # Process command
        if command.lower() == 'help':
            self.cmd_output.insert(tk.END, "Available Commands:\n")
            self.cmd_output.insert(tk.END, "  activate - Activate covenant loop\n")
            self.cmd_output.insert(tk.END, "  status - Show system status\n")
            self.cmd_output.insert(tk.END, "  optimize - Optimize parameters\n")
            self.cmd_output.insert(tk.END, "  pulse - Pulse center node\n")
            self.cmd_output.insert(tk.END, "  clear - Clear output\n\n")

        elif command.lower() == 'activate':
            self.activate_covenant()

        elif command.lower() == 'status':
            self.show_status()

        elif command.lower() == 'optimize':
            self.optimize_params()

        elif command.lower() == 'pulse':
            self.activate_center_node()
            self.cmd_output.insert(tk.END, "✓ Center node pulsed\n\n")

        elif command.lower() == 'clear':
            self.cmd_output.delete(1.0, tk.END)

        else:
            self.cmd_output.insert(tk.END, f"Unknown command. Type 'help' for options.\n\n")

        self.cmd_output.see(tk.END)
        self.log_to_scroll(f"Command: {command}")

    def activate_covenant(self):
        """Activate covenant loop from command."""
        intent = self.intent_var.get()
        self.cmd_output.insert(tk.END, f"🔥 Activating covenant with intent: {intent}\n")

        try:
            response = requests.post(f'{API_BASE}/covenant/activate',
                json={'intent': intent, 'invocation': 'CLI activation'})

            if response.ok:
                data = response.json()
                if data.get('success'):
                    result = data.get('result', {})
                    steps = result.get('steps', {})

                    self.cmd_output.insert(tk.END, "✓ Covenant activated successfully\n")

                    if 'choose' in steps:
                        model = steps['choose'].get('selected_model', 'unknown')
                        self.cmd_output.insert(tk.END, f"  Model: {model}\n")

                    if 'calibrate' in steps:
                        mix = steps['calibrate'].get('optimized_mix', 0)
                        self.cmd_output.insert(tk.END, f"  Mix: {mix:.2f}\n")

                    self.cmd_output.insert(tk.END, "\n")
                else:
                    self.cmd_output.insert(tk.END, "❌ Activation failed\n\n")
        except:
            self.cmd_output.insert(tk.END, "⚠ API offline - cannot activate\n\n")

    def show_status(self):
        """Show system status."""
        try:
            response = requests.get(f'{API_BASE}/covenant/status')
            if response.ok:
                data = response.json()
                self.cmd_output.insert(tk.END, f"Status: {'Active' if data.get('active') else 'Idle'}\n")
                self.cmd_output.insert(tk.END, f"Active loops: {data.get('active_loops', 0)}\n\n")
        except:
            self.cmd_output.insert(tk.END, "⚠ API offline\n\n")

    def optimize_params(self):
        """Optimize parameters."""
        intent = self.intent_var.get()
        self.cmd_output.insert(tk.END, f"✨ Optimizing for {intent}...\n")

        try:
            response = requests.post(f'{API_BASE}/parameters/optimize',
                json={'intent': intent})

            if response.ok:
                data = response.json()
                if data.get('success'):
                    params = data.get('optimized_parameters', {})
                    self.cmd_output.insert(tk.END, f"✓ Mix: {params.get('optimized_mix', 0):.2f}\n")
                    self.cmd_output.insert(tk.END, f"✓ Gain: {params.get('optimized_gain', 0):.2f}\n")
                    self.cmd_output.insert(tk.END, f"✓ Resonance: {params.get('optimized_resonance', 0):.2f}\n\n")
        except:
            self.cmd_output.insert(tk.END, "⚠ API offline\n\n")

    def update_status_loop(self):
        """Background thread to update status."""
        while self.running:
            time.sleep(5)
            # Could ping API for updates here

    def on_closing(self):
        """Cleanup on close."""
        self.running = False
        self.root.destroy()


def run_sophia_shell():
    """Main entry point."""
    root = tk.Tk()
    app = SophiaShell(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    run_sophia_shell()
