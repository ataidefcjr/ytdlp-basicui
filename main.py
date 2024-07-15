import tkinter as tk
from tkinter import messagebox, Text, Button, Label, Entry, filedialog
import subprocess
import threading
import sys

class YtDlpInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("YTDLP Basic Interface")

        # Centralizar a janela principal
        window_width = 680
        window_height = 350
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        master.resizable(False,False)

        # Carregar último diretório usado ou definir diretório inicial
        self.last_output_dir = self.load_last_directory()
        self.output_dir_var = tk.StringVar(value=self.last_output_dir)

        # Label e Text para URL
        self.url_label = Label(master, text="URL(s):")
        self.url_label.grid(row=0, column=0, sticky=tk.E)
        
        self.url_text = Text(master, height=10, width=50)
        self.url_text.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Label e Entry para argumentos personalizados
        self.args_label = Label(master, text="Custom Arguments:")
        self.args_label.grid(row=1, column=0, sticky="e")
        
        self.args_entry = Entry(master, width=50, bd=3, relief=tk.GROOVE)
        self.args_entry.grid(row=1, column=1, padx=5, sticky="ew")

        # Botão de ajuda para argumentos
        self.help_button = Button(master, text="Help", height=3, width=25, command=self.show_help)
        self.help_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Label e Entry para seleção de diretório de saída
        self.output_label = Label(master, text="Output Folder:", width=30)
        self.output_label.grid(row=2, column=0, sticky="e")
        
        self.output_entry = Entry(master, textvariable=self.output_dir_var, width=50, bd=3, relief=tk.GROOVE)
        self.output_entry.grid(row=2, column=1, padx=5, sticky="ew")
        
        self.output_button = Button(master, text="Select Output Folder", width=25, height=3, command=self.choose_output_directory)
        self.output_button.grid(row=2, column=2, pady=10, padx=10, sticky="ew")

        # Botão para iniciar o download
        self.download_button = Button(master, text="Download", height=3, command=self.start_downloads)
        self.download_button.grid(row=3, column=0, columnspan=3, padx=80, pady=10, sticky="ew")

        # Configuração de expansão das células para ocupar todo o espaço disponível
        for i in range(4):
            master.grid_rowconfigure(i, weight=1)
        for j in range(3):
            master.grid_columnconfigure(j, weight=1)

    def load_last_directory(self):
        try:
            with open("last_directory.txt", "r") as f:
                last_dir = f.read().strip()
                return last_dir
        except FileNotFoundError:
            return ""

    def save_last_directory(self, directory):
        with open("last_directory.txt", "w") as f:
            f.write(directory)

    def choose_output_directory(self):
        # Abre a janela de seleção de diretório
        output_dir = filedialog.askdirectory(initialdir=self.last_output_dir)
        if output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_dir)
            self.save_last_directory(output_dir)

    def show_help(self):
        # Mensagem de ajuda para os argumentos
        help_text = (
            "-f FORMAT (defines video format)\n"
            "-x (convert to audio)\n"
            "--audio-format FORMAT (converts to specified format)\n"
            "\nEnter URLs separated by line breaks"
        )
        messagebox.showinfo("HELP - Arguments", help_text)

    def start_downloads(self):
        # Obter URLs e argumentos personalizados
        urls = self.url_text.get("1.0", tk.END).strip().split("\n")
        args = self.args_entry.get()
        output_dir = self.output_entry.get()

        # Verificar se pelo menos uma URL foi inserida
        if not any(urls):
            messagebox.showerror("Error", "Please enter at least one URL.")
            return

        # Verificar se o diretório de saída foi selecionado
        if not output_dir:
            messagebox.showerror("Error", "Please select the output directory.")
            return

        # Minimizar a janela principal
        self.master.withdraw()

        # Exibir mensagem de aguarde
        wait_message = tk.Toplevel(self.master)
        wait_message.title("Wait")
        label = tk.Label(wait_message, text="Downloading videos, please wait...")
        label.pack(padx=20, pady=20)

        # Centralizar a janela de aguarde
        window_width = 300
        window_height = 100
        screen_width = wait_message.winfo_screenwidth()
        screen_height = wait_message.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        wait_message.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Verificar se estamos no Windows
        is_windows = sys.platform.startswith('win')

        # Construir o comando yt-dlp
        command = ['-m', 'yt_dlp', *urls, '-o', f'{output_dir}/%(title)s.%(ext)s']
        if is_windows:
            command.insert(0, 'pythonw')
            command.append('--windows-filenames')
        else:
            command.insert(0, 'python3')
        if args:
            command.extend(args.split())

        # Iniciar download em uma thread separada
        threading.Thread(target=self.execute_download, args=(command, wait_message), daemon=True).start()

    def execute_download(self, command, wait_message):
        try:
            # Executar o comando
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()

            # Fechar mensagem de aguarde ao término
            wait_message.destroy()

            # Restaurar a janela principal ao término
            self.master.deiconify()

            if process.returncode != 0:
                messagebox.showerror("Error", f"Error downloading videos:\n{stderr}")
            else:
                messagebox.showinfo("Sucess", "All downloads are complete!")

        except Exception as e:
            messagebox.showerror("Error", f"Error from yt-dlp:\n{str(e)}")

def main():
    root = tk.Tk()
    app = YtDlpInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
