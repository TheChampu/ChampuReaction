import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message
from Champu import Champu

server_result_template = (
    "✯ sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs ✯\n\n"
    "ᴄʟɪᴇɴᴛ:\n"
    "» ɪsᴩ: {isp}\n"
    "» ᴄᴏᴜɴᴛʀʏ: {country}\n\n"
    "sᴇʀᴠᴇʀ:\n"
    "» ɴᴀᴍᴇ: {server_name}\n"
    "» ᴄᴏᴜɴᴛʀʏ: {server_country}, {server_cc}\n"
    "» sᴩᴏɴsᴏʀ: {sponsor}\n"
    "» ʟᴀᴛᴇɴᴄʏ: {latency} ms\n"
    "» ᴩɪɴɢ: {ping} ms"
)

def run_speedtest():
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    results = test.results.dict()
    share_link = test.results.share() if test.results.share() else None
    results["share"] = share_link
    return results

@Champu.on_message(filters.command(["speedtest", "spt"], prefixes=["/"]))
async def speedtest_function(client, message: Message):
    m = await message.reply_text("ʀᴜɴɴɪɴɢ ꜱᴩᴇᴇᴅ...")
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_speedtest)

        output = server_result_template.format(
            isp=result["client"]["isp"],
            country=result["client"]["country"],
            server_name=result["server"]["name"],
            server_country=result["server"]["country"],
            server_cc=result["server"]["cc"],
            sponsor=result["server"]["sponsor"],
            latency=result["server"]["latency"],
            ping=result["ping"],
        )

        if result["share"]:
            await message.reply_photo(photo=result["share"], caption=output)
        else:
            await message.reply_text(output)

        await m.delete()
    except Exception as e:
        await m.edit_text(f"Error: {e}")
