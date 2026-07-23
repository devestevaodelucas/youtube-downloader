import yt_dlp
import os

def listar_qualidades(url):
    with yt_dlp.YoutubeDL({'quiet': True, 'extractor_args': {'youtube': {'js_runtimes': ['node']}}}) as ydl:
        info = ydl.extract_info(url, download=False)
        formatos = []
        vistos = set()

        for f in info['formats']:
            qualidade = f.get('format_note')
            ext = f.get('ext')
            if qualidade and ext == 'mp4' and qualidade not in vistos:
                formatos.append({'id': f['format_id'], 'qualidade': qualidade})
                vistos.add(qualidade)

        return formatos, info['title']

def baixar_video(url, format_id):
    os.makedirs('videos', exist_ok=True)
    opcoes = {
        'format': f'{format_id}+bestaudio[ext=m4a]/bestaudio',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'extractor_args': {'youtube': {'js_runtimes': ['node']}},
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])

# --- Programa principal ---
while True:
    url = input("\nCole o link do vídeo do YouTube (ou digite 'sair' para fechar): ")

    if url.lower() == 'sair':
        print("👋 Até mais!")
        break

    if '&list=' in url:
        url = url.split('&list=')[0]
        print(f"✂️ Link limpo automaticamente: {url}")

    formatos, titulo = listar_qualidades(url)

    print(f"\nVídeo: {titulo}")
    print("\nQualidades disponíveis:")
    for i, f in enumerate(formatos):
        print(f"{i + 1}. {f['qualidade']}")

    escolha = int(input("\nEscolha o número da qualidade: ")) - 1
    format_id = formatos[escolha]['id']

    print("\nBaixando...")
    baixar_video(url, format_id)
    print("✅ Download concluído! O vídeo foi salvo na pasta 'videos'!")