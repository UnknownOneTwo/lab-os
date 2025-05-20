#!/usr/bin/env python3

import os
import subprocess
import requests
import platform
import csv
from datetime import datetime

OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://192.168.10.125:11434/api/generate"
CSV_DIR = "/root/lab-tag-history"
os.makedirs(CSV_DIR, exist_ok=True)

version = datetime.now().strftime("v%Y%m%d-%H%M%S")
CSV_OUTPUT = os.path.join(CSV_DIR, f"proxmox_tag_notes_{version}.csv")
LATEST_LINK = os.path.join(CSV_DIR, "latest.csv")


def get_vm_list():
    result = subprocess.run(["qm", "list"], capture_output=True, text=True)
    return parse_proxmox_list(result.stdout, "VM")


def get_ct_list():
    result = subprocess.run(["pct", "list"], capture_output=True, text=True)
    return parse_proxmox_list(result.stdout, "CT")


def parse_proxmox_list(raw, type_label):
    lines = raw.strip().split("\n")
    if len(lines) < 2:
        print(f"⚠️ No entries found for {type_label}.")
        return []
    headers = lines[0].split()
    entries = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < len(headers):
            continue
        entry = dict(zip(headers, parts))
        entry['TYPE'] = type_label
        entries.append(entry)
    return entries


def get_config_summary(entry):
    vmid = entry['VMID']
    try:
        if entry['TYPE'] == "VM":
            result = subprocess.run(["qm", "config", vmid], capture_output=True, text=True)
        else:
            result = subprocess.run(["pct", "config", vmid], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"❌ Failed to get config for {entry['TYPE']} {vmid}: {e}")
        return ""


def prompt_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()['response']


def build_prompt(vmid, name, type_label, config_text):
    return f"""
Here is a Proxmox {type_label} configuration:
- Name: {name}
- ID: {vmid}
- Type: {type_label}
- Config:
{config_text}

Suggest a set of 2-4 lowercase tags (comma separated) that are helpful in a homelab context. Then write a short, user-friendly summary (2-3 sentences max) explaining what this machine is for, written like a helpful lab note.

Reply in this format:
Tags: tag1, tag2, tag3
Notes: <brief, casual explanation>
"""


def apply_tags(vmid, type_label, tags):
    cmd = ["qm" if type_label == "VM" else "pct", "set", vmid, "--tags", tags]
    subprocess.run(cmd)


def apply_description(vmid, type_label, description):
    cmd = ["qm" if type_label == "VM" else "pct", "set", vmid, "--description", description]
    subprocess.run(cmd)


def run():
    print("🔍 Collecting VM and CT information from Proxmox...")
    entries = get_vm_list() + get_ct_list()
    results = []

    for entry in entries:
        vmid = entry['VMID']
        name = entry.get('Name', f"{entry['TYPE'].lower()}-{vmid}")
        type_label = entry['TYPE']
        print(f"🤖 Processing {type_label} {vmid} ({name})...")

        config_text = get_config_summary(entry)
        if not config_text.strip():
            print(f"⚠️ Skipping {type_label} {vmid} — empty config.")
            continue

        print(f"📄 Config Summary for {vmid} ({type_label}):\n{config_text}")

        prompt = build_prompt(vmid, name, type_label, config_text)
        response = prompt_ollama(prompt)

        print(f"🧠 Ollama Response for {vmid}:\n{response}")

        lines = response.strip().split("\n")
        tags = next((l.replace("Tags:", "").strip() for l in lines if l.lower().startswith("tags:")), "")
        notes = next((l.replace("Notes:", "").strip() for l in lines if l.lower().startswith("notes:")), "")

        print(f"🔖 Applying tags: {tags}")
        print(f"🗒️ Applying notes: {notes}")

        apply_tags(vmid, type_label, tags)
        apply_description(vmid, type_label, notes)

        results.append({
            "VMID": vmid,
            "Name": name,
            "Type": type_label,
            "Tags": tags,
            "Notes": notes
        })

    print(f"📝 Writing results to {CSV_OUTPUT}...")
    with open(CSV_OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["VMID", "Name", "Type", "Tags", "Notes"])
        writer.writeheader()
        writer.writerows(results)

    print("📝 Writing to latest.csv...")
    with open(LATEST_LINK, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["VMID", "Name", "Type", "Tags", "Notes"])
        writer.writeheader()
        writer.writerows(results)

    print("✅ Tagging and notes complete!")
    print(f"📂 Version: {version}")


if __name__ == "__main__":
    run()
