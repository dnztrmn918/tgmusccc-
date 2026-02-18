#!/bin/bash
# Eski pyrogram'ı kaldır ve pyrofork kur
pip uninstall pyrogram -y 2>/dev/null || true
pip install --no-cache-dir pyrofork==2.3.58
pip install --no-cache-dir -r requirements.txt
python3 -m bot
