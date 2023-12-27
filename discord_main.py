import base64
import io

from dbctrl import get_random_question, get_random_exam_table_name
import info
import private

import discord
from discord import Option

# 鍵設定
DISCORD_SERVER_IDs = private.DISCORD_SERVER_IDs
TOKEN = private.TOKEN

client = discord.Bot()
 
@client.event
async def on_ready():
    print(f"{client.user} WAITING CMD...")


@client.slash_command(description="1問ランダム出題", guild_ids=DISCORD_SERVER_IDs)
async def output_random_question(
    ctx: discord.ApplicationContext,
    category: Option(str, required=False, description="T=テクニカル, M=マネジメント, S=ストラテジ"),
):
    # テーブル取得
    table_name = get_random_exam_table_name()
    # 問題選択
    row = get_random_question(table_name)
    
    # base64 -> jpg
    img_binary = base64.b64decode(row[info.ENUM_COLUMNS_QUESTION_BASE64])
    image_stream = io.BytesIO(img_binary)
    image_stream.seek(0)

    # Discordフォーマットに変換
    file = discord.File(image_stream, filename="question.jpg")

    # 問題送信
    await ctx.respond(f"From {table_name} question No.{row[info.ENUM_COLUMNS_ID]}, answer:||{row[info.ENUM_COLUMNS_ANSWER]}||")
    msg = await ctx.send(file=file)

    # 選択肢のリアクション追加
    for choice in ['\U0001f1e6', '\U0001f1ee', '\U0001f1fa', '\U0001f1ea']:
        await msg.add_reaction(choice)


if __name__ == '__main__':
    client.run(TOKEN)
