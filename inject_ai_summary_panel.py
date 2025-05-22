import os
import argparse

AI_NAV_HTML = """
<li><a href=\"#ai-summary\">AI Summary</a></li>
""".strip()

AI_PANEL_HTML = """
<article id=\"ai-summary\">
  <h2 class=\"major\">AI System Summary</h2>
  <span class=\"image main\"><img src=\"images/pic03.jpg\" alt=\"AI panel\" /></span>
  <div id=\"summary-content\">
    <p><em>Loading AI-generated summary from Ollama...</em></p>
  </div>
</article>
""".strip()

AI_JS = """
<script>
  fetch('index.md')
    .then(response => response.text())
    .then(text => {
      const summaryBlock = document.getElementById('summary-content');
      summaryBlock.innerHTML = text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
        .replace(/\n/gim, '<br />');
    })
    .catch(err => {
      document.getElementById('summary-content').innerHTML =
        '<p>⚠️ Error loading AI summary.</p>';
    });
</script>
""".strip()

def inject_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "id=\"ai-summary\"" in content:
        print("✅ AI Summary panel already exists. Skipping injection.")
        return

    # Inject nav link
    content = content.replace('</ul>', f'  {AI_NAV_HTML}\n</ul>')

    # Inject article before closing </div> in <div id="main">
    content = content.replace('</div>', f'{AI_PANEL_HTML}\n</div>', 1)

    # Inject JS before </body>
    content = content.replace('</body>', f'{AI_JS}\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ AI Summary panel injected into: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject AI summary panel into HTML.")
    parser.add_argument('--target', required=True, help="Path to index.html")
    args = parser.parse_args()

    inject_content(args.target)
