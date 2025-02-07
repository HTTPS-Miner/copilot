import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import html2text  # Markdown'a dönüştürme için html2text modülü

# Tarayıcı seçenekleri
options = uc.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Onur\AppData\Local\Google\Chrome\User Data")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-popup-blocking")

# Tarayıcıyı başlat
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 10)

def wait_for_page_load(driver, timeout=15):
    """Sayfanın tamamen yüklenmesini bekler."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def wait_for_complete_response(driver, class_name, old_texts, timeout=30, check_interval=2):
    """Yeni cevabın tamamen yüklenmesini bekler ve HTML içeriğini döndürür."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.CLASS_NAME, class_name)) > len(old_texts)
        )
        element = driver.find_elements(By.CLASS_NAME, class_name)[-1]

        previous_html = ""
        elapsed_time = 0

        while elapsed_time < timeout:
            current_html = element.get_attribute("outerHTML")

            if current_html.strip() and current_html != previous_html:
                previous_html = current_html
                time.sleep(check_interval)
                elapsed_time += check_interval
            else:
                break  

        # Eğer içerik tamamlandıysa, onu döndür
        return previous_html if previous_html.strip() else None
    except:
        return None

# Mevcut sekmeyi kullanarak Copilot'a git
driver.get("https://copilot.microsoft.com/")
wait_for_page_load(driver)

# Mesaj gönderme
with open("messagetobesent.txt", "r", encoding="utf-8") as file:
    mesaj = file.read().strip()

max_retries = 5
retry_count = 0
copilot_html = None

while retry_count < max_retries:
    try:
        textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        textarea.click()
        textarea.send_keys(mesaj)
        textarea.send_keys(Keys.ENTER)
        
        previous_copilot_responses = driver.find_elements(By.CLASS_NAME, "space-y-3")
        copilot_html = wait_for_complete_response(driver, "space-y-3", previous_copilot_responses)
        break  
    except:
        print(f"Copilot mesaj kutusu bulunamadı, tekrar deniyorum ({retry_count+1}/{max_retries})...")
        retry_count += 1
        time.sleep(3)

# Copilot yanıtını kaydetme
html_output_dir = "answer/html_responses"
os.makedirs(html_output_dir, exist_ok=True)

if copilot_html:
    html_file_path = f"{html_output_dir}/copilot_answer.html"
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(copilot_html)
else:
    print("Copilot yanıtı alınamadı.")

# HTML içeriğini Markdown'a dönüştürme
def convert_html_to_markdown(html_content):
    return html2text.html2text(html_content)

# Markdown dosyasını oluştur
if copilot_html:
    markdown_output_dir = "answer/markdown_responses"
    os.makedirs(markdown_output_dir, exist_ok=True)
    
    markdown_content = convert_html_to_markdown(copilot_html)
    md_file_path = os.path.join(markdown_output_dir, "copilot_answer.md")
    
    with open(md_file_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    print(f"✔️ Markdown dosyası oluşturuldu: {md_file_path}")

# Tarayıcıyı kapat
driver.quit()