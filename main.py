import nextcord
from nextcord.ext import commands
import json
from lib.helpers import get_all_posts, Vars,converter,is_cashed,setInterval

from dotenv import load_dotenv
load_dotenv()
get_all_posts


class MeowerBot(commands.Bot):
    def __init__(self, prefix="MeowerBot!",discription=None ,**options):
        chc = self.Check_for_message_in_fs()
        super().__init__(prefix, discription,**options)

    
    async def on_guild_available(self, guild: nextcord.guild) -> None:
        posts = get_all_posts()
        msgs,guild = Vars(posts)
        converted_msgs = converter(msgs)
        del posts
        del msgs
        for channel in guild.channels:
           
                for i,msg in enumerate(converted_msgs):
                    if channel.id == msg["chat_id"]:
                        sg = channel.send_message(f"::{msg['user']} : {msg['mesg']}")
                        msg['chat_id'] = sg.id
                    channel.send_message(msg)
        self.Cashe_messages('bot_storage/guilds.json',converted_msgs,guild)
    
    @setInterval(5)
    def Check_for_message_in_fs(self):
        
        raise NotImplementedError(self.Check_for_message_in_fs)
    
    @staticmethod
    def Cashe_messages(json_file_path,converted_msgs,guild):
        with open(json_file_path, "r") as f:
            data = json.load(f)


        for i,msg in enumerate(converted_msgs):
            if not is_cashed(msg,guild):
                data[guild].append(msg)

        
        with open(json_file_path, "w") as f:
            json.dump(data, f)       


bot = MeowerBot()