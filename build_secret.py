#!/usr/bin/env python3
import os
import base64
import getpass
import sys

def rc4(key_bytes, data_bytes):
    S = list(range(256))
    j = 0
    out = bytearray(len(data_bytes))
    
    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
        
    # Pseudo-random generation algorithm (PRGA)
    i = 0
    j = 0
    for k in range(len(data_bytes)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out[k] = data_bytes[k] ^ S[(S[i] + S[j]) % 256]
        
    return bytes(out)

def main():
    raw_path = os.path.join("secret_src", "secret_raw.html")
    out_path = "secret.html"
    
    if not os.path.exists(raw_path):
        print(f"❌ Ошибка: Файл {raw_path} не найден!")
        sys.exit(1)
        
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_html = f.read()
        
    print("🔒 Сборщик секретной страницы secret.html")
    if len(sys.argv) > 1:
        password = sys.argv[1].strip()
    else:
        password = getpass.getpass("Введите пароль шифрования: ").strip()
        if not password:
            print("❌ Ошибка: Пароль не может быть пустым!")
            sys.exit(1)
            
        confirm_pass = getpass.getpass("Подтвердите пароль шифрования: ").strip()
        if password != confirm_pass:
            print("❌ Ошибка: Пароли не совпадают!")
            sys.exit(1)
        
    print("⏳ Шифрование страницы...")
    key_bytes = password.encode("utf-8")
    data_bytes = raw_html.encode("utf-8")
    encrypted_bytes = rc4(key_bytes, data_bytes)
    base64_str = base64.b64encode(encrypted_bytes).decode("utf-8")
    
    stub_html = f'''<!DOCTYPE html>
<html lang="ru">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Geologica:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap"
    rel="stylesheet">
  <link rel="stylesheet" href="css/style.css?v=5">
  <style>
    .lock-screen {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background-color: var(--background);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 2000;
      padding: 1.5rem;
    }}

    .lock-card {{
      background-color: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 3rem 2.5rem;
      box-shadow: var(--shadow-md);
      text-align: center;
      max-width: 420px;
      width: 100%;
      position: relative;
      overflow: hidden;
      transition: var(--transition-smooth);
    }}

    .lock-card:hover {{
      box-shadow: 0 12px 30px rgba(244, 63, 94, 0.15);
      border-color: rgba(244, 63, 94, 0.3);
    }}

    .lock-input {{
      width: 100%;
      padding: 0.85rem 1rem;
      border-radius: var(--radius-md);
      border: 1px solid var(--border);
      background-color: var(--input-background);
      color: var(--foreground);
      margin-bottom: 0.5rem;
      text-align: center;
      font-size: 1.15rem;
      letter-spacing: 0.15em;
      font-weight: 700;
      transition: var(--transition-smooth);
    }}

    .lock-input:focus {{
      border-color: #f43f5e;
      background-color: var(--card);
      box-shadow: 0 0 0 3px rgba(244, 63, 94, 0.15);
    }}

    .lock-btn {{
      width: 100%;
      padding: 0.85rem;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #f43f5e, #ec4899);
      color: white;
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 1rem;
      cursor: pointer;
      border: none;
      transition: var(--transition-smooth);
      margin-top: 0.5rem;
    }}

    .lock-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(244, 63, 94, 0.3);
    }}

    .lock-error {{
      color: #ef4444;
      font-size: 0.875rem;
      margin-top: 0.5rem;
      min-height: 1.25rem;
      font-weight: 500;
    }}
  </style>
</head>

<body>
  <!-- Lock Screen Dialog -->
  <div id="lock-screen" class="lock-screen">
    <div class="lock-card">
      <span style="font-size: 3.5rem; animation: pulseHeart 1.5s infinite alternate; display: inline-block;">🔒</span>
      <h2 style="font-family: var(--font-heading); font-size: 1.75rem; margin-top: 1rem; background: linear-gradient(135deg, #f43f5e, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Тайная комната</h2>
      <p style="font-size: 0.95rem; margin-bottom: 1.5rem; color: var(--foreground); opacity: 0.9;">Введите секретный ключ, чтобы войти в наше пространство ✨</p>
      <input type="password" id="password-input" class="lock-input" placeholder="КЛЮЧ" autofocus>
      <button id="unlock-btn" class="lock-btn">Войти 💖</button>
      <div id="lock-error" class="lock-error"></div>
    </div>
  </div>

  <script>
    (function() {{
      const savedTheme = localStorage.getItem('theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {{
        document.body.classList.add('dark-theme');
      }}

      const ENCRYPTED_PAGE_BASE64 = "{base64_str}";

      function rc4(keyBytes, dataBytes) {{
        const s = new Uint8Array(256);
        for (let i = 0; i < 256; i++) s[i] = i;
        let j = 0;
        for (let i = 0; i < 256; i++) {{
          j = (j + s[i] + keyBytes[i % keyBytes.length]) % 256;
          const temp = s[i]; s[i] = s[j]; s[j] = temp;
        }}
        let i = 0; j = 0;
        const result = new Uint8Array(dataBytes.length);
        for (let k = 0; k < dataBytes.length; k++) {{
          i = (i + 1) % 256;
          j = (j + s[i]) % 256;
          const temp = s[i]; s[i] = s[j]; s[j] = temp;
          result[k] = dataBytes[k] ^ s[(s[i] + s[j]) % 256];
        }}
        return result;
      }}

      function decryptPage(base64Data, password) {{
        const binaryString = atob(base64Data);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {{
          bytes[i] = binaryString.charCodeAt(i);
        }}
        const keyBytes = new TextEncoder().encode(password);
        const decryptedBytes = rc4(keyBytes, bytes);
        return new TextDecoder().decode(decryptedBytes);
      }}

      const passwordInput = document.getElementById('password-input');
      const unlockBtn = document.getElementById('unlock-btn');
      const lockError = document.getElementById('lock-error');

      function tryUnlock() {{
        const password = passwordInput.value.trim();
        if (!password) {{
          lockError.textContent = "Введите пароль! 🥺";
          return;
        }}
        lockError.textContent = "";
        unlockBtn.disabled = true;
        unlockBtn.textContent = "Расшифровка...";

        setTimeout(() => {{
          try {{
            const decryptedHtml = decryptPage(ENCRYPTED_PAGE_BASE64, password);
            if (!decryptedHtml || !decryptedHtml.includes("<!DOCTYPE html>")) {{
              throw new Error("Invalid password");
            }}

            // Parse decrypted HTML into DOM
            const parser = new DOMParser();
            const doc = parser.parseFromString(decryptedHtml, 'text/html');

            const secretContainer = doc.getElementById('secret-container');
            if (!secretContainer) {{
              throw new Error("Invalid page structure");
            }}

            // Swap document head and body
            document.head.innerHTML = doc.head.innerHTML;
            document.body.innerHTML = doc.body.innerHTML;

            // Re-execute scripts dynamically
            const scripts = doc.querySelectorAll('script');
            scripts.forEach(oldScript => {{
              const newScript = document.createElement('script');
              Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
              newScript.textContent = oldScript.textContent;
              document.body.appendChild(newScript);
            }});
          }} catch (err) {{
            console.error(err);
            lockError.textContent = "Неверный секретный ключ! Попробуй еще раз... 🥺";
            passwordInput.value = "";
            passwordInput.focus();
            unlockBtn.disabled = false;
            unlockBtn.textContent = "Войти 💖";
          }}
        }}, 50);
      }}

      unlockBtn.addEventListener('click', tryUnlock);
      passwordInput.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter') tryUnlock();
      }});
    }})();
  </script>
</body>
</html>'''

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(stub_html)
        
    print(f"✨ Успешно! {raw_path} зашифрован в {out_path}.")

if __name__ == "__main__":
    main()
