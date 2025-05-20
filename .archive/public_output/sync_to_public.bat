@echo off
echo 🧹 Running sanitize_for_public.py...
python sanitize_for_public.py

echo 🚚 Copying sanitized files to public repo...
robocopy public_output ..\homelab-automation-kit /MIR

cd ..\homelab-automation-kit

echo 📦 Committing and pushing to GitHub...
git add .
git commit -m "🔄 Weekly sync from private repo"
git push

echo ✅ Sync complete!
pause
