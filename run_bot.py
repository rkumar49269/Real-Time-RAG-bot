import subprocess
import time
import os

print("⚙️ Running System Diagnostics & Repair...")

# 1. Check if Ollama is installed
if os.system("which ollama > /dev/null") != 0:
    print("❌ Ollama not found. Re-installing...")
    os.system("curl -fsSL https://ollama.com/install.sh | sh")
else:
    print("✅ Ollama is installed.")

# 2. Kill any old processes to free up ports
os.system("pkill ollama")
os.system("pkill streamlit")
os.system("pkill cloudflared")
time.sleep(2)

# 3. Start Ollama Server
print("🔄 Starting AI Server...")
subprocess.Popen("nohup ollama serve > ollama.log 2>&1 &", shell=True)
time.sleep(5)  # Wait for it to boot

# 4. Check & Pull Model (This is usually why it hangs!)
print("📥 Verifying Llama 3 Model (This might take a minute)...")
# We try to pull. If it exists, it checks mostly instantly. If missing, it downloads.
os.system("ollama pull llama3:8b")

# 5. Start Streamlit App
print("🚀 Launching App...")
if not os.path.exists("app.py"):
    print("⚠️  app.py missing! Please re-run the cell that creates 'app.py'.")
else:
    subprocess.Popen(["streamlit", "run", "app.py", "--server.port=8501"])
    time.sleep(3)

    # 6. Start Cloudflare Tunnel (Stable Connection)
    print("\n🔗  OPEN THIS LINK TO CHAT:")
    # Ensure cloudflared is available
    if os.system("which cloudflared > /dev/null") != 0:
        os.system("wget -q -O cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb")
        os.system("dpkg -i cloudflared.deb")
    os.system("cloudflared tunnel --url http://localhost:8501")