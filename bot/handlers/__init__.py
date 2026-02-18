from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

def register_handlers(app: Client):
    """Tüm handler'ları kaydet"""
    from .start import start_command
    from .play import play_command
    from .controls import pause_command, resume_command, stop_command
    from .queue import queue_command
    
    # Handler'ları ekle
    app.add_handler(MessageHandler(start_command, filters.command("start") & filters.private))
    app.add_handler(MessageHandler(play_command, filters.command("play") & filters.group))
    app.add_handler(MessageHandler(pause_command, filters.command("pause") & filters.group))
    app.add_handler(MessageHandler(resume_command, filters.command("resume") & filters.group))
    app.add_handler(MessageHandler(stop_command, filters.command("stop") & filters.group))
    app.add_handler(MessageHandler(queue_command, filters.command("queue") & filters.group))
