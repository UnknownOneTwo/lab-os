import datetime

# Mock system log and Ollama output for now
LOG_FILE = "system_updates.log"
OUTPUT_FILE = "index.md"

# Simulate an AI summary generation
def generate_summary(log_path):
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            summary = "\n".join([f"- {line.strip()}" for line in lines if line.strip()])
            return f"## LabOS Summary – {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + summary
    except FileNotFoundError:
        return "## LabOS Summary\n\n⚠️ No log data found."

def write_summary_to_index(summary):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(summary)

if __name__ == "__main__":
    summary = generate_summary(LOG_FILE)
    write_summary_to_index(summary)
    print(f"✅ index.md updated with AI summary.")
