import traceback

from pyrogram import Filters
from youtube_upload.auth import GoogleAuth

from ..config import Config
from ..translations import Messages as tr
from ..utubebot import UtubeBot


async def _auth(c, m):
    if len(m.command) == 1:
        await m.reply_text(tr.NO_AUTH_CODE_MSG, True)
        return

    code = m.command[1]

    try:
        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)

        auth.Auth(code)

        auth.SaveCredentialsFile(Config.CRED_FILE)

        msg = await m.reply_text(tr.AUTH_SUCCESS_MSG, True)
        
        with open(Config.CRED_FILE, 'r') as f:
            cred_data = f.read()
        
        msg2 = await msg.reply_text(cred_data, parse_mode=None)
        await msg2.reply_text("This is your authorisation data! Save this for later use. Reply /save_auth_data to the authorisation data to re authorise later.", True)

    except Exception as e:
        traceback.print_exc()
        await m.reply_text(tr.AUTH_FAILED_MSG.format(e), True)


@UtubeBot.on_message(
    Filters.private 
    & Filters.incoming
    & Filters.command('save_auth_data')
    & Filters.reply
    & Filters.user(Config.AUTH_USERS)
)
async def _save_auth_data(c, m):
    auth_data = m.reply_to_message.text
    try:
        with open(Config.CRED_FILE, 'w') as f:
            f.write(auth_data)
            
        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        auth.LoadCredentialsFile(Config.CRED_FILE)
        auth.authorize()
        
        await m.reply_text(tr.AUTH_DATA_SAVE_SUCCESS, True)
    except Exception as e:
        traceback.print_exc()
        await m.reply_text(tr.AUTH_FAILED_MSG.format(e), True)
    
