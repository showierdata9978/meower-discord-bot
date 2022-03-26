from lib.toberemoved.filesystem import Files

from lib.toberemoved.suporter import Supporter
import json

import threading
supporter = Supporter()
filesystem = Files(
    logger = supporter.log,
    errorhandler = supporter.full_stack
)
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    try:
                        function(*args, **kwargs)
                    except NotImplementedError:
                        supporter.log.error("NotImplementedError")
                        pass
            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

def fetch_post_from_storage(post_id):
    if filesystem.does_file_exist("/Storage/Categories/Home/Messages/", post_id):
        result, payload = filesystem.load_file("/Storage/Categories/Home/Messages/{0}".format(post_id))
        
        if result:
            if ("isDeleted" in payload) and (payload["isDeleted"]):
                payload = {
                    "isDeleted": True
                }
                
            else:
                payload["isDeleted"] = False
        
        return True, result, payload
    else:
        return True, False, {}


def get_all_message_files():
    return filesystem.get_all_files_in_directory("/Storage/Categories/Home/Messages/")

def get_all_posts():
    all_posts = []
    for post_id in get_all_message_files():
        result, payload = fetch_post_from_storage(post_id)
        
        if result:
            if not payload["isDeleted"]:
                continue

        all_posts.append(payload)
    return all_posts


def Vars(posts):
    
    msgs1 = []
    for i,post in enumerate(posts):
        msgs1.append({
            "mesg": post["p"],
            "user": post["u"],
            "chat_id": post["chatid"],
            "post_id": post["post_id"],
            "state": post['state']
        })
    return msgs1


def converter(msgs,guid_id):
    # Add discord channel id to the dict
    # make it possible to have more then 1 guild in the bot

    with open('guilds.json', 'r') as f:
        guilds = json.load(f)
    for guild in guilds:
        if guild["guid"]['id'] == guid_id:
            dataConvert =  guild['dataConvert']
            guild1 = guild
            break
    #Converting Meower Data to Discord Data
    for i,msg in enumerate(msgs):
        msgs[i]["chat_id"] = dataConvert[int(msg["chat_id"])]
    return msgs,guild1  

def is_cashed(msg,guild):
   
    for m in guild['cashaed_msgs']:
        if m["post_id"] == msg["post_id"]:
            return True
    return False
