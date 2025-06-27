from pyrogram import Client, filters
import aiohttp
import os
import asyncio

API_ENDPOINT = "http://152.42.164.96:8001/api/upscale"

BOT_TOKEN = "8005957715:AAF3S9sYdNcaRBYt9FiDaCLe7aO6P70wXew"
API_ID = 20457610
API_HASH = "b7de0dfecd19375d3f84dbedaeb92537"

app = Client("test", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("upscale") & filters.reply)
async def upscale(client, message):
    reply = message.reply_to_message

    if not reply.photo:
        await message.reply_text("❌ Pehle kisi photo ko reply karke upscale likho.")
        return

    downloading_msg = await message.reply_text("📤 Upscaling started...")

    file_path = await client.download_media(reply.photo.file_id)

    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                data = aiohttp.FormData()
                data.add_field("file", f, filename=os.path.basename(file_path), content_type="image/jpeg")
                data.add_field("scale", "4")

                async with session.post(API_ENDPOINT, data=data) as resp:
                    if resp.status == 200:
                        image_bytes = await resp.read()
                        await message.reply_photo(image_bytes, caption="✅ Upscaled successfully!")
                    else:
                        await message.reply_text(f"❌ Upscaling failed with status {resp.status}.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")
    finally:
        await downloading_msg.delete()
        os.remove(file_path)

async def main():
    await app.start()
    print("Bot is running...")
    await asyncio.Event().wait()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
