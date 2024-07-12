import tkinter as tk
from tkinter import messagebox, Text, Button, Label, Entry, filedialog
import subprocess
import threading

class YtDlpInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("yt-dlp Interface")

        # Centralizar a janela principal
        window_width = 600
        window_height = 400
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Carregar último diretório usado ou definir diretório inicial
        self.last_output_dir = self.load_last_directory()
        self.output_dir_var = tk.StringVar(value=self.last_output_dir)

        # Label e Text para URL
        self.url_label = Label(master, text="URL(s) do Vídeo:")
        self.url_label.grid(row=0, column=0, sticky=tk.E)

        self.url_text = Text(master, height=10, width=50)
        self.url_text.grid(row=0, column=1, columnspan=2, pady=10)

        # Label e Entry para argumentos personalizados
        self.args_label = Label(master, text="Argumentos Personalizados:")
        self.args_label.grid(row=1, column=0, sticky=tk.E)
        self.args_entry = Entry(master, width=50)
        self.args_entry.grid(row=1, column=1, pady=10)

        # Botão de ajuda para argumentos
        self.help_button = Button(master, text="Ajuda", command=self.show_help)
        self.help_button.grid(row=1, column=2, padx=5, pady=10)

        # Label e Entry para seleção de diretório de saída
        self.output_label = Label(master, text="Diretório de Saída:")
        self.output_label.grid(row=2, column=0, sticky=tk.E)
        self.output_entry = Entry(master, textvariable=self.output_dir_var, width=40)
        self.output_entry.grid(row=2, column=1, pady=10)
        self.output_button = Button(master, text="Selecionar", command=self.choose_output_directory)
        self.output_button.grid(row=2, column=2, pady=10)

        # Botão para iniciar o download
        self.download_button = Button(master, text="Baixar Vídeos", command=self.start_downloads)
        self.download_button.grid(row=3, column=1, pady=20)

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
            "-f FORMATO (formato de vídeo)\n"
            "-x (converte para áudio)\n"
            "--audio-format FORMATO (converte para o formato especificado)"
        )
        messagebox.showinfo("Ajuda - Argumentos", help_text)

    def start_downloads(self):
        # Obter URLs e argumentos personalizados
        urls = self.url_text.get("1.0", tk.END).strip().split("\n")
        args = self.args_entry.get()
        output_dir = self.output_entry.get()

        # Verificar se pelo menos uma URL foi inserida
        if not any(urls):
            messagebox.showerror("Erro", "Por favor, insira pelo menos uma URL.")
            return

        # Verificar se o diretório de saída foi selecionado
        if not output_dir:
            messagebox.showerror("Erro", "Por favor, selecione um diretório de saída.")
            return

        # Minimizar a janela principal
        self.master.withdraw()

        # Exibir mensagem de aguarde
        wait_message = tk.Toplevel(self.master)
        wait_message.title("Aguarde")
        label = tk.Label(wait_message, text="Baixando vídeos, por favor, aguarde...")
        label.pack(padx=20, pady=20)

        # Centralizar a janela de aguarde
        window_width = 300
        window_height = 100
        screen_width = wait_message.winfo_screenwidth()
        screen_height = wait_message.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        wait_message.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Construir o comando yt-dlp
        command = ['yt-dlp', *urls, '-o', f'{output_dir}/%(title)s.%(ext)s', '--windows-filenames']
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
                messagebox.showerror("Erro", f"Erro ao baixar vídeos:\n{stderr}")
            else:
                messagebox.showinfo("Sucesso", "Todos os downloads foram concluídos!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar yt-dlp:\n{str(e)}")

def main():
    root = tk.Tk()
    app = YtDlpInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
