from flask import Flask, render_template_string, redirect, url_for
import os
import subprocess
import markdown
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kgotlaai-secret"

DASHBOARD_MD = "dashboard_output/DAILY_DASHBOARD.md"
ADMIN_SCRIPT = "admin_dashboard.py"

def get_dashboard_html():
    if os.path.exists(DASHBOARD_MD):
        with open(DASHBOARD_MD, "r", encoding="utf-8") as f:
            return markdown.markdown(f.read(), extensions=['tables', 'fenced_code'])
    return "<h2>Dashboard not generated yet. Click Run Agents.</h2>"

@app.route("/")
def index():
    html = get_dashboard_html()
    return f'''
    <!DOCTYPE html>
    <html><head><title>Kgotla AI Live Dashboard</title>
    <style>@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap");
    body {{font-family:"Inter",sans-serif;background:#0f172a;color:#e2e8f0;margin:0;padding:0;}}
    .header {{background:#1e2937;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center;}}
    .btn {{padding:14px 28px;background:#22c55e;color:#000;font-weight:600;border:none;border-radius:8px;cursor:pointer;}}
    .btn:hover {{background:#86efac;}}
    .container {{max-width:1200px;margin:2rem auto;padding:0 2rem;}}
    .card {{background:#1e2937;border-radius:12px;padding:2rem;box-shadow:0 10px 15px -3px rgb(0 0 0 / 0.3);}}
    </style></head><body>
    <div class="header"><h1>🚀 Kgotla AI - LIVE COMMAND DASHBOARD</h1>
    <button onclick="runNow()" class="btn">RUN ALL AGENTS NOW</button></div>
    <div class="container">
      <div class="card">
        <p><strong>Last updated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M SAST")}</p>
        <div style="background:#0f172a;padding:1.5rem;border-radius:8px;overflow:auto;max-height:80vh;">{html}</div>
      </div>
    </div>
    <script>
    function runNow() {{
      if(confirm("Run all agents now?")) {{
        fetch("/run", {{method:"POST"}}).then(()=>location.reload());
      }}
    }}
    </script>
    </body></html>
    '''

@app.route("/run", methods=["POST"])
def run():
    try:
        subprocess.run(["python", ADMIN_SCRIPT], cwd=".", check=True)
    except:
        pass
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
