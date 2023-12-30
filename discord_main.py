import base64
import io
import datetime

from dbctrl import get_random_question, get_random_exam_table_name
import info
import private

import discord
from discord import Option
from discord.ext import tasks

# 鍵設定
DISCORD_SERVER_IDs = private.DISCORD_SERVER_IDs
TOKEN = private.TOKEN

client = discord.Bot()
 
@client.event
async def on_ready():
    print(f"{client.user} WAITING CMD...")


# 手動実行
@client.slash_command(description="1問ランダム出題", guild_ids=DISCORD_SERVER_IDs)
async def output_random_question(
    ctx: discord.ApplicationContext,
    # category: Option(str, required=False, description="T=テクニカル, M=マネジメント, S=ストラテジ"),
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


#定期実行用
send_allow = True # 1日おきにサーバが再起動する前提のため、ここ以外でTrueにセットしない
@tasks.loop(seconds=5)
async def cyclic_output_random_question():
    global send_allow
    # JST = UTC + 9h
    dt_now_jst = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
    # print(dt_now_jst.strftime("%H:%M"))

    # 22:00 なら実行
    if send_allow:
        if dt_now_jst.hour == 22 and dt_now_jst.minute == 00:
            send_allow = False
            channel = client.get_channel(private.CHANNEL_IDs[0])

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
            msg = await channel.send(
                content=f"From {table_name} question No.{row[info.ENUM_COLUMNS_ID]}, answer:||{row[info.ENUM_COLUMNS_ANSWER]}||",
                file=file,
            )

            # 選択肢のリアクション追加
            for choice in ['\U0001f1e6', '\U0001f1ee', '\U0001f1fa', '\U0001f1ea']:
                await msg.add_reaction(choice)

if __name__ == '__main__':
    cyclic_output_random_question.start()
    client.run(TOKEN)
