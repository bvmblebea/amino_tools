import asyncio
import aminofix.asyncfix
from . import menu_configs
from tabulate import tabulate
client = aminofix.asyncfix.Client()

# -- auth and other functions --


async def auth():
    while True:
        try:
            email = input("Email >> ")
            password = input("Password >> ")
            await client.login(email=email, password=password)
            return False
        except Exception as e:
            print(e)


async def communities():
    try:
        clients = await client.sub_clients(start=0, size=100)
        for x, name in enumerate(clients.name, 1):
            print(f"{x}.{name}")
        while True:
            com_Id = clients.comId[int(input("Select the community >> ")) - 1]
            return com_Id
    except (ValueError, TypeError):
        communities()
    except Exception as e:
        print(e)


async def chats(sub_client: aminofix.asyncfix.SubClient):
    try:
        chats = await sub_client.get_chat_threads(size=100)
        for z, title in enumerate(chats.title, 1):
            print(f"{z}.{title}")
        while True:
            chat_Id = chats.chatId[int(input("Select the chat >> ")) - 1]
            return chat_Id
    except (ValueError, TypeError):
        return
    except Exception as e:
        print(e)

        # -- auth and other functions --

        # -- spam tools --


async def spam_bot(message: str):
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    chatId = await chats(sub_client=sub_client)
    while True:
        await sub_client.send_message(message=message, chatId=chatId, messageType=0)
        print(">> Message Sent...")


async def wiki_spam_bot(message: str):
    link_Info = await client.get_from_code(input("Wiki Link >> "))
    wiki_Id = link_Info.wikiId
    com_Id = link_Info.comId
    sub_client = await aminofix.asyncfix.SubClient(comId=com_Id, profile=client.profile)
    while True:
        await sub_client.comment(message=message, wikiId=wiki_Id)
        print(">> Comment Sent...")


async def wall_spam_bot(message: str):
    link_Info = await client.get_from_code(input("User Link >> "))
    user_Id = link_Info.objectId
    com_Id = link_Info.comId
    sub_client = await aminofix.asyncfix.SubClient(comId=com_Id, profile=client.profile)
    while True:
        await sub_client.comment(message=message, userId=user_Id)
        print(">> Comment Sent...")


async def blog_spam_bot(message: str):
    link_Info = await client.get_from_code(input("Blog Link >> "))
    blog_Id = link_Info.objectId
    com_Id = link_Info.comId
    sub_client = await aminofix.asyncfix.SubClient(comId=com_Id, profile=client.profile)
    while True:
        await sub_client.comment(message=message, blogId=blog_Id)
        print(">> Comment Sent...")

        # -- spam tools --

        # -- chat tools --


async def chat_Id_finder():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    print(tabulate(menu_configs.chat_Id_finder_menu, tablefmt="psql"))
    select = input("Select >> ")
    if select == "1":
        print(">> Public Chats ChatId::: ")
        public_chats = await sub_client.get_public_chat_threads(size=100)
        for title, chat_Id in zip(public_chats.title, public_chats.chatId):
            print(f"{title} >> {chat_Id}")

    elif select == "2":
        print(">> Joined Chats ChatId::: ")
        joined_chats = await sub_client.get_chat_threads(size=100)
        for title, chat_Id in zip(joined_chats.title, joined_chats.chatId):
            print(f"{title} >> {chat_Id}")


async def crash_chat_description():
    link_Info = await client.get_from_code(input("Chat Link >> "))
    chat_Id = link_Info.objectId
    com_Id = link_Info.comId
    sub_client = await aminofix.asyncfix.SubClient(comId=com_Id, profile=client.profile)
    content = open("crash_description.txt").read()
    await sub_client.edit_chat(content=content, chatId=chat_Id, viewOnly="yes")


async def transfer_fake_coins():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    chat_Id = await chats(sub_client=sub_client)
    coins = input("Coins Count >> ")
    await sub_client.send_coins(chatId=chat_Id, coins=1)
    while True:
        await sub_client.send_coins(chatId=chat_Id, coins=coins)
        print(">> Sent Fake Coins...")

        # -- chat tools --

        # -- activity tools --


async def chat_invite_bot():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    chat_Id = await chats(sub_client=sub_client)
    print(tabulate(menu_configs.chat_invite_bot_menu, tablefmt="psql"))
    select = input("Select >> ")

    async def invite_online_users():
        for i in range(0, 2000, 250):
            try:
                users_list = await sub_client.get_online_users(start=i, size=100)
                online_users = [*users_list.profile.userId]
                print(">> Inviting Online Users...")
                await asyncio.gather(*[asyncio.create_task(sub_client.invite_to_chat(user_Id, chat_Id)) for user_Id in online_users])
            except BaseException:
                continue
        print(">> Invited Online Users...")

    async def invite_recent_users():
        for i in range(0, 2000, 250):
            try:
                users_list = await sub_client.get_all_users(type="recent", start=i, size=100)
                recent_users = [*users_list.profile.userId]
                print(">> Inviting Recent Users...")
                await asyncio.gather(*[asyncio.create_task(sub_client.invite_to_chat(user_Id, chat_Id)) for user_Id in recent_users])
            except BaseException:
                continue
        print(">> Invited Recent Users...")

    if select == "1":
        await invite_online_users()
    elif select == "2":
        await invite_recent_users()


async def like_bot():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    blogs_count = int(input("Blogs Count (Min - 1/Max - 100) >> "))
    for i in range(0, 2000, 250):
        recent_blogs = await sub_client.get_recent_blogs(start=i, size=blogs_count).blogId
        for blog_Id in recent_blogs:
            await sub_client.like_blog(blogId=blog_Id)
            print(f">> Liked {blog_Id}")


async def follow_bot():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    print(tabulate(menu_configs.follow_bot_menu, tablefmt="psql"))
    select = input("Select >> ")

    if select == "1":
        for i in range(0, 2000, 250):
            try:
                users_list = await sub_client.get_online_users(start=i, size=100)
                online_users = [*users_list.profile.userId]
                print(">> Following To Online Users...")
                await asyncio.gather(*[asyncio.create_task(sub_client.follow(user_Id)) for user_Id in online_users])
            except BaseException:
                continue
        print(">> Followed To Online Users...")

    elif select == "2":
        for i in range(0, 2000, 250):
            try:
                users_list = await sub_client.get_all_users(type="recent", start=i, size=100)
                recent_users = [*users_list.profile.userId]
                print(">> Following To Recent Users...")
                await asyncio.gather(*[asyncio.create_task(sub_client.follow(user_Id)) for user_Id in recent_users])
            except BaseException:
                continue
        print(">> Followed To Recent Users...")


async def unfollow_bot():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    users_list = await sub_client.get_user_following(userId=sub_client.profile.userId, size=100)
    followed_users = [*users_list.profile.userId]
    print(">> Unfollowing From Followed Users...")
    await asyncio.gather(*[asyncio.create_task(sub_client.unfollow(user_Id)) for user_Id in followed])

    # -- activity tools --

    # -- profile tools --


async def blogs_spam(title: str, content: str):
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    while True:
        await sub_client.post_blog(title=title, content=content, backgroundColor="#C0C0C0")
        print(">> Created Blog...")


async def wikis_spam(title: str, content: str):
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    while True:
        await sub_client.post_wiki(title=title, content=content, backgroundColor="#C0C0C0")
        print(">> Created Wiki...")

        # -- profile tools --

        # -- raid tools __


async def spam_system_messages():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    chat_Id = await chats(sub_client=sub_client)
    message = input("Message >> ")
    message_type = input("Message Type >> ")
    while True:
        print(">> Spamming...")
        await asyncio.gather(*[asyncio.create_task(sub_client.send_message(chat_Id, message, message_type)) for _ in range(500)])


async def send_system_message(message: str):
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    chat_Id = await chats(sub_client=sub_client)
    message_type = input("Message Type >> ")
    while True:
        try:
            for i in range(1):
                await sub_client.send_message(chatId=chat_Id, message=message, messageType=message_type)
        except Exception as e:
            print(e)


async def join_leave(sub_client: aminofix.asyncfix.SubClient, chat_Id: str):
    await sub_client.leave_chat(chatId=chat_Id)
    await sub_client.join_chat(chatId=chat_Id)


async def spam_with_join_leave():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    chat_Id = await chats(sub_client=sub_client)
    while True:
        print(">> Spamming With Join And Leave...")
        await asyncio.gather(*[asyncio.create_task(join_leave(sub_client, chat_Id)) for _ in range(500)])


async def ip_recipient():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    wallet_history = await sub_client.get_wallet_history(size=100)
    for i in range(50):
        if wallet_history.changedCoins[i] > 0:
            if wallet_history.description[i] is not None:
                print(wallet_history.description[i])
                print(f"Ip >> {wallet_history.sourceIp[i]}")


async def join_active_chats():
    sub_client = await aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    public_chats = await sub_client.get_public_chat_threads(size=100).chatId
    for chat_Id in public_chats:
        print(">> Joining In Public Chats...")
        await asyncio.gather(*[asyncio.create_task(sub_client.join_chat(chat_Id))])

        # -- raid tools --

        # -- main start function --


async def main():
    await auth()
    print(tabulate(menu_configs.main_menu, tablefmt="psql"))
    select = input("Select >> ")

    if select == "1":
        print(tabulate(menu_configs.spam_tools_menu, tablefmt="psql"))
        select = input("Select >> ")

        if select == "1":
            await spam_bot(message=input("Message >> "))

        elif select == "2":
            await wiki_spam_bot(message=input("Message >> "))

        elif select == "3":
            await wall_spam_bot(message=input("Message >> "))

        elif select == "4":
            await blog_spam_bot(message=input("Message >> "))

        elif select == "0":
            exit()

    elif select == "2":
        print(tabulate(menu_configs.chat_tools_menu, tablefmt="psql"))
        select = input("Select >> ")

        if select == "1":
            await chat_Id_finder()

        elif select == "2":
            await crash_chat_description()

        elif select == "3":
            await transfer_fake_coins()

        elif select == "0":
            exit()

    elif select == "3":
        print(
            tabulate(
                menu_configs.activity_tools_menu,
                tablefmt="psql"))
        select = input("Select >> ")

        if select == "1":
            await chat_invite_bot()

        elif select == "2":
            await like_bot()

        elif select == "3":
            await follow_bot()

        elif select == "4":
            await unfollow_bot()

        elif select == "0":
            exit()

    elif select == "4":
        print(tabulate(menu_configs.profile_tools_menu, tablefmt="psql"))
        select = input("Select >> ")

        if select == "1":
            await blogs_spam()

        elif select == "2":
            await wiki_spam()

        elif select == "0":
            exit()

    elif select == "5":
        print(tabulate(menu_configs.raid_tools_menu, tablefmt="psql"))
        select = input("Select >> ")

        if select == "1":
            await spam_system_messages()

        elif select == "2":
            await send_system_message(message=input("Message >> "))

        elif select == "3":
            await spam_with_join_leave()

        elif select == "4":
            await ip_recipient()

        elif select == "5":
            await join_active_chats(sub_client=sub_client)

        elif select == "0":
            exit()

    elif select == "0":
        exit()

# End...
