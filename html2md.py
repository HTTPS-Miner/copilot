import os
import html2text

# HTML ve Markdown dosyalarının konumu
INPUT_DIR = "answer/html_responses"
OUTPUT_DIR = "answer/markdown_responses"

# Çıkış klasörünü oluştur
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_html_to_markdown(html_file, md_file):
    """Verilen HTML dosyasını okuyup Markdown formatına çevirir ve kaydeder."""
    try:
        # HTML dosyasını oku
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()
        
        # HTML içeriğini Markdown'a dönüştür
        markdown_content = html2text.html2text(html_content)
        
        # Markdown içeriğini dosyaya kaydet
        with open(md_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        
        print(f"✔️ Markdown dosyası oluşturuldu: {md_file}")
    except Exception as e:
        print(f"❌ Hata: {e}")

# Tüm HTML dosyalarını dönüştür
if os.path.exists(INPUT_DIR):  # INPUT_DIR var mı kontrol et
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".html"):
            html_path = os.path.join(INPUT_DIR, filename)
            md_filename = filename.replace(".html", ".md")
            md_path = os.path.join(OUTPUT_DIR, md_filename)
            
            convert_html_to_markdown(html_path, md_path)
else:
    print(f"❌ {INPUT_DIR} dizini bulunamadı.")
