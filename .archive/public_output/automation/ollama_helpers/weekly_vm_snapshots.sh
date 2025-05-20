#!/bin/bash
# weekly_vm_snapshots.sh
# Creates weekly snapshots of all VMs and CTs on the Proxmox node

DATE=$(date +%Y%m%d-%H%M)
LOGFILE="/root/lab-tag-history/snapshot_log_$DATE.txt"

echo "📦 Weekly Snapshot Started at $DATE" > "$LOGFILE"

# Snapshot all VMs
for VMID in $(qm list | awk 'NR>1 {print $1}'); do
  NAME=$(qm config $VMID | grep '^name:' | awk '{print $2}')
  SNAPSHOT_NAME="weekly-$DATE"
  echo "🧠 Creating VM snapshot: $VMID ($NAME) - $SNAPSHOT_NAME" >> "$LOGFILE"
  qm snapshot $VMID $SNAPSHOT_NAME -description "Automated weekly snapshot created at $DATE" >> "$LOGFILE" 2>&1
done

# Snapshot all containers
for CTID in $(pct list | awk 'NR>1 {print $1}'); do
  NAME=$(pct config $CTID | grep '^hostname:' | awk '{print $2}')
  SNAPSHOT_NAME="weekly-$DATE"
  echo "🧠 Creating CT snapshot: $CTID ($NAME) - $SNAPSHOT_NAME" >> "$LOGFILE"
  pct snapshot $CTID $SNAPSHOT_NAME -description "Automated weekly snapshot created at $DATE" >> "$LOGFILE" 2>&1
done

echo "✅ Weekly Snapshot Completed" >> "$LOGFILE"
