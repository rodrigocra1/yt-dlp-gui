#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading


class YtDlpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Gráfica para yt-dlp")
        self.root.geometry("700x600")
        self.root.minsize(500, 450)

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL
        url_frame = ttk.LabelFrame(main_frame, text="URL do Vídeo")
        url_frame.pack(fill=tk.X, padx=5, pady=5)

        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.fetch_button = ttk.Button(url_frame, text="Buscar Formatos", command=self.fetch_formats_threaded)
        self.fetch_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Opções
        options_frame = ttk.LabelFrame(main_frame, text="Opções de Download")
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(options_frame, text="Qualidade de Vídeo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.quality_var = tk.StringVar()
        self.quality_menu = ttk.Combobox(options_frame, textvariable=self.quality_var, state="disabled")
        self.quality_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(options_frame, text="Codec de Vídeo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.codec_var = tk.StringVar()
        self.codec_menu = ttk.Combobox(options_frame, textvariable=self.codec_var, state="disabled")
        self.codec_menu.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        self.audio_only_var = tk.BooleanVar()
        self.audio_only_check = ttk.Checkbutton(options_frame, text="Somente Áudio", variable=self.audio_only_var,
                                                command=self.toggle_video_options)
        self.audio_only_check.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Label(options_frame, text="Qualidade de Áudio:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.audio_quality_var = tk.StringVar()
        self.audio_quality_menu = ttk.Combobox(options_frame, textvariable=self.audio_quality_var, state="disabled")
        self.audio_quality_menu.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(options_frame, text="Idioma do Áudio (ex: pt, en):").grid(row=4, column=0, padx=5, pady=5,
                                                                            sticky=tk.W)
        self.audio_language_entry = ttk.Entry(options_frame, width=10)
        self.audio_language_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.audio_language_entry.insert(0, "pt")

        options_frame.columnconfigure(1, weight=1)

        # Pasta de Saída
        output_frame = ttk.LabelFrame(main_frame, text="Pasta de Saída")
        output_frame.pack(fill=tk.X, padx=5, pady=5)

        self.output_path_var = tk.StringVar()
        self.output_path_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=50)
        self.output_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.output_path_button = ttk.Button(output_frame, text="Selecionar Pasta", command=self.select_output_folder)
        self.output_path_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Download e Progresso
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        self.status_label = ttk.Label(action_frame, text="Insira uma URL e clique em 'Buscar Formatos'",
                                      anchor="center")
        self.status_label.pack(fill=tk.X, pady=(5, 10))

        self.progress_bar = ttk.Progressbar(action_frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.download_button = ttk.Button(action_frame, text="Baixar", command=self.start_download, state="disabled")
        self.download_button.pack(pady=10)

    def fetch_formats_threaded(self):
        threading.Thread(target=self.fetch_formats, daemon=True).start()

    def fetch_formats(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL.")
            return

        self.fetch_button.config(state="disabled")
        self.download_button.config(state="disabled")
        self.status_label.config(text="Buscando formatos, por favor aguarde...")
        self.root.update_idletasks()

        try:
            ydl_opts = {'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get('formats', [])

            video_resolutions = sorted(
                list(set([f['height'] for f in formats if f.get('vcodec') != 'none' and f.get('height') is not None])))
            raw_video_codecs = sorted(
                list(set([f['vcodec'] for f in formats if f.get('vcodec') not in ['none', None]])))
            audio_bitrates = sorted(
                list(set([int(f['abr']) for f in formats if f.get('acodec') != 'none' and f.get('abr') is not None])),
                reverse=True)

            codec_map = {'avc': 'h264', 'h264': 'h264', 'hev': 'h265', 'hevc': 'h265', 'vp9': 'vp9', 'av01': 'AV1'}
            ordered_friendly_codecs = []
            for raw_codec in raw_video_codecs:
                found_friendly_name = False
                for key, value in codec_map.items():
                    if key in raw_codec.lower():
                        ordered_friendly_codecs.append(value)
                        found_friendly_name = True
                        break
                if not found_friendly_name:
                    ordered_friendly_codecs.append(raw_codec)

            final_codec_list = list(dict.fromkeys(ordered_friendly_codecs))
            self.codec_menu['values'] = final_codec_list

            self.quality_menu['values'] = [f'{res}p' for res in video_resolutions]
            self.audio_quality_menu['values'] = [f'{abr}k' for abr in audio_bitrates]

            if video_resolutions:
                self.quality_var.set(f'{video_resolutions[-1]}p')
                self.quality_menu.config(state="readonly")

            if final_codec_list:
                default_codec = "h264" if "h264" in final_codec_list else final_codec_list[0]
                self.codec_var.set(default_codec)
                self.codec_menu.config(state="readonly")

            if audio_bitrates:
                self.audio_quality_var.set(f'{audio_bitrates[0]}k')
                self.audio_quality_menu.config(state="readonly")

            if not video_resolutions and not audio_bitrates:
                self.status_label.config(text="Nenhum formato de vídeo ou áudio encontrado.")
                messagebox.showerror("Erro", "Não foi possível encontrar formatos válidos para esta URL.")
            else:
                self.status_label.config(text="Formatos encontrados. Selecione as opções e a pasta de saída.")
                self.download_button.config(state="normal")

            self.toggle_video_options()

        except Exception as e:
            self.status_label.config(text="Erro ao buscar formatos.")
            messagebox.showerror("Erro ao Buscar Formatos", f"Ocorreu um erro:\n{e}")
        finally:
            self.fetch_button.config(state="normal")

    def toggle_video_options(self):
        if self.audio_only_var.get() and self.quality_menu['values']:
            self.quality_menu.config(state="disabled")
            self.codec_menu.config(state="disabled")
        elif self.quality_menu['values']:
            self.quality_menu.config(state="readonly")
            self.codec_menu.config(state="readonly")

    def select_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_path_var.set(folder_selected)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes_str = d.get('_total_bytes_str', 'N/A')
            percent_str = d.get('_percent_str', '0.0%').strip()
            speed_str = d.get('_speed_str', 'N/A')

            try:
                percentage = float(percent_str.replace('%', ''))
                self.progress_bar['value'] = percentage
            except ValueError:
                pass

            self.status_label.config(text=f"Baixando: {percent_str} de {total_bytes_str} a {speed_str}")
            self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.status_label.config(text="Download concluído. Mesclando formatos...")
            self.progress_bar['value'] = 100
            self.root.update_idletasks()

    def download_thread(self):
        url = self.url_entry.get()
        output_path = self.output_path_var.get()

        if not url or not output_path:
            messagebox.showerror("Erro", "URL e Pasta de Saída são obrigatórias.")
            return

        quality = self.quality_var.get().replace('p', '')
        codec = self.codec_var.get()
        audio_quality = self.audio_quality_var.get().replace('k', '')
        audio_language = self.audio_language_entry.get().strip().lower()

        try:
            ydl_opts = {
                'progress_hooks': [self.progress_hook],
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'noplaylist': True,
            }

            # --- CORREÇÃO: Lógica de seleção de formato mais tolerante a falhas ---
            video_selector = "bestvideo"
            video_filters = []
            if quality:
                video_filters.append(f"height<={quality}")
            if codec:
                video_filters.append(f"vcodec~={codec}")
            if video_filters:
                video_selector = f"bestvideo[{']['.join(video_filters)}]"

            audio_selector = "bestaudio"
            audio_filters = []
            if audio_quality:
                audio_filters.append(f"abr>={audio_quality}")
            if audio_language:
                # Usar '?' para indicar que o filtro é opcional/preferencial
                audio_filters.append(f"lang~={audio_language}?")
            if audio_filters:
                audio_selector = f"bestaudio[{']['.join(audio_filters)}]"

            # Formato final com múltiplos fallbacks para máxima robustez
            if self.audio_only_var.get():
                ydl_opts['format'] = f'{audio_selector}/bestaudio'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
            else:
                ydl_opts['format'] = f"{video_selector}+{audio_selector}/bestvideo+bestaudio/best"
                ydl_opts['merge_output_format'] = 'mp4'
            # --- FIM DA CORREÇÃO ---

            self.download_button.config(state="disabled")
            self.fetch_button.config(state="disabled")
            self.progress_bar['value'] = 0
            self.status_label.config(text="Iniciando download...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.status_label.config(text="Download e processamento concluídos!")
            messagebox.showinfo("Sucesso", "Download concluído com sucesso!")

        except Exception as e:
            self.status_label.config(text="Erro durante o download.")
            messagebox.showerror("Erro no Download", str(e))
        finally:
            self.download_button.config(state="normal")
            self.fetch_button.config(state="normal")
            self.progress_bar['value'] = 0

    def start_download(self):
        threading.Thread(target=self.download_thread, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = YtDlpApp(root)
    root.mainloop()