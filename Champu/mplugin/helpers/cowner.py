from Champu import db, SUDOERS
from config import OWNER_ID

cloneownerdb = db.clone_owners

async def get_clone_owner(bot_id):
    data = await cloneownerdb.find_one({"bot_id": bot_id})
    if data:
        return data["user_id"]
    return None
    
async def is_owner(bot_id, user_id):
    owner_id = await get_clone_owner(bot_id)
    if owner_id == user_id or user_id == OWNER_ID or user_id in SUDOERS:
        return True
    return False
