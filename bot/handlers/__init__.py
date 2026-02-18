from pyrogram import Client, filters
from pyrogram.types import Message

def register_handlers(app: Client):
    """Tüm handler'ları kaydet"""
    from .start import start_command
    from .play import play_command
    from .controls import pause_command, resume_command, stop_command
    from .queue import queue_command
    
    app.add_handler(start_command)
    app.add_handler(play_command)
    app.add_handler(pause_command)
    app.add_handler(resume_command)
    app.add_handler(stop_command)
    app.add_handler(queue_command)
