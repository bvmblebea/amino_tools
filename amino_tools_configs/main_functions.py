import amino
from . import menu_configs
from tabulate import tabulate
from asyncio import gather, create_task

client = amino.AsyncClient()

		# -- auth and other functions --


async def auth():
    while True:
        try:
            email = input("-- Email::: ")
            password = input("-- Password::: ")
            await client.login(email=email, password=password)
            return False
        except Exception as e:
            print(e)


async def communities():
	while True:
		try:
			clients = await client.sub_clients(start=0, size=100)
			for x, name in enumerate(clients.name, 1):
				print(f"-- {x}:{name}")
			com_id = clients.comId[int(input("-- Select the community::: ")) - 1]
			return com_id
		except Exception as e:
			print(e)


async def chats(sub_client: amino.AsyncSubClient):
    while True:
    	try:
    		chats = await sub_client.get_chat_threads(size=100)
    		for z, title in enumerate(chats.title, 1):
    			print(f"-- {z}:{title}")
    		chat_id = chats.chatId[int(input("-- Select the chat::: ")) - 1]
    		return chat_id
    	except Exception as e:
    		print(e)

        # -- auth and other functions --


        # -- spam tools --

async def spam_bot(sub_client: amino.AsyncSubClient):
    chat_id = await chats(sub_client=sub_client)
    message = input("-- Message::: ")
    while True:
        await sub_client.send_message(message=message, chatId=chat_id, messageType=0)
        print("-- Message is sent...")


async def wiki_spam_bot(sub_client: amino.AsyncSubClient):
    link_info = await client.get_from_code(input("-- Wiki Link::: "))
    wiki_id = link_info.wikiId
    message = input("-- Message::: ")
    while True:
        await sub_client.comment(message=message, wikiId=wiki_id)
        print("-- Comment is sent...")


async def wall_spam_bot(sub_client: amino.AsyncSubClient):
    link_info = await client.get_from_code(input("-- User Link::: "))
    user_id = link_info.objectId
    message = input("-- Message::: ")
    while True:
        await sub_client.comment(message=message, userId=user_id)
        print("-- Comment is sent...")


async def blog_spam_bot(sub_client: amino.AsyncSubClient):
    link_info = await client.get_from_code(input("-- Blog Link::: "))
    blog_id = link_info.objectId
    message = input("-- Message::: ")
    while True:
        await sub_client.comment(message=message, blogId=blog_id)
        print("-- Comment is sent...")

        # -- spam tools --


        # -- chat tools --

async def chat_id_finder(sub_client: amino.AsyncSubClient):
    print(tabulate(menu_configs.chat_id_finder_menu, tablefmt="psql"))
    select = int(input("-- Select::: "))
    if select == 1:
        print("-- Public chats chat_ids:::")
        public_chats = await sub_client.get_public_chat_threads(size=100)
        for title, chat_id in zip(public_chats.title, public_chats.chatId):
            print(f"-- {title}:{chat_id}")

    elif select == 2:
        print("-- Joined chats chat_ids:::")
        joined_chats = await sub_client.get_chat_threads(size=100)
        for title, chat_id in zip(joined_chats.title, joined_chats.chatId):
            print(f"-- {title}:{chat_id}")


async def crash_chat_description(sub_client: amino.AsyncSubClient):
    link_info = await client.get_from_code(input("-- Chat Link::: "))
    chat_id = link_info.objectId
    content = open("crash_description.txt").read()
    await sub_client.edit_chat(content=content, chatId=chat_id, viewOnly="yes")


async def transfer_fake_coins(sub_client: amino.AsyncSubClient):
    chat_id = await chats(sub_client=sub_client)
    coins = int(input("-- How many fake coins?(min - 1/max - 500)::: "))
    await sub_client.send_coins(chatId=chat_id, coins=1)
    while True:
        await sub_client.send_coins(chatId=chat_id, coins=coins)
        print(">> Fake coins is sent...")

        # -- chat tools --


        # -- activity tools --

async def chat_invite_bot(sub_client: amino.AsyncSubClient):
    chat_id = await chats(sub_client=sub_client)
    print(tabulate(menu_configs.chat_invite_bot_menu, tablefmt="psql"))
    select = int(input("-- Select::: "))

    async def invite_online_users():
        for i in range(0, 2000, 15000):
            try:
                users_list = await sub_client.get_online_users(start=i, size=100)
                online_users = [*users_list.profile.userId]
                print("-- Inviting online users...")
                await gather(
                    *[
                        create_task(sub_client.invite_to_chat(user_id, chat_id))
                        for user_id in online_users
                    ]
                )
            except BaseException:
                continue
        print("-- Invited online users...")

    async def invite_recent_users():
        for i in range(0, 2000, 15000):
            try:
                users_list = await sub_client.get_all_users(
                    type="recent", start=i, size=100
                )
                recent_users = [*users_list.profile.userId]
                print("-- Inviting recent users...")
                await gather(
                    *[
                        create_task(sub_client.invite_to_chat(user_id, chat_id))
                        for user_id in recent_users
                    ]
                )
            except BaseException:
                continue
        print("-- Invited recent users...")

    if select == 1:
        await invite_online_users()

    elif select == 2:
        await invite_recent_users()


async def like_bot(sub_client: amino.AsyncSubClient):
    for i in range(0, 2000, 10000):
        recent_blogs = await sub_client.get_recent_blogs(start=i, size=100).blogId
        for blog_id in recent_blogs:
            await sub_client.like_blog(blogId=blog_id)
            print(f"-- Liked::: {blog_id}")


async def follow_bot(sub_client: amino.AsyncSubClient):
    print(tabulate(menu_configs.follow_bot_menu, tablefmt="psql"))
    select = int(input("-- Select::: "))

    if select == 1:
        for i in range(0, 2000, 15000):
            try:
                users_list = await sub_client.get_online_users(start=i, size=100)
                online_users = [*users_list.profile.userId]
                print("-- Following to online users...")
                await gather(
                    *[
                        create_task(sub_client.follow(user_id))
                        for user_id in online_users
                    ]
                )
            except BaseException:
                continue
        print("-- Followed fo online users...")

    elif select == 2:
        for i in range(0, 2000, 15000):
            try:
                users_list = await sub_client.get_all_users(
                    type="recent", start=i, size=100
                )
                recent_users = [*users_list.profile.userId]
                print("-- Following to recent users...")
                await gather(
                    *[
                        create_task(sub_client.follow(user_id))
                        for user_id in recent_users
                    ]
                )
            except BaseException:
                continue
        print("-- Followed to recent users...")


async def unfollow_bot(sub_client: amino.AsyncSubClient):
    while True:
        following_users_count = sub_client.get_user_info(
            userId=sub_client.profile.userId
        ).followingCount
        if following_users_count > 0:
            for i in range(0, following_users_count, 100):
                followed_users = await sub_client.get_user_following(
                    userId=sub_client.profile.userId, size=100
                ).profile.userId
                if followed_users:
                    await gather(
                        *[
                            create_task(sub_client.unfollow(user_id))
                            for user_id in followed_users
                        ]
                    )
                    print("-- Unfollowing from followed users...")

                # -- activity tools --

                # -- profile tools --


async def blogs_spam(sub_client: amino.AsyncSubClient):
    title = input("-- Title::: ")
    content = input("-- Content::: ")
    while True:
        await sub_client.post_blog(
            title=title, content=content, backgroundColor="#C0C0C0"
        )
        print("-- Created blog...")


async def wikis_spam(sub_client: amino.AsyncSubClient):
    title = input("-- Title::: ")
    content = input("-- Content::: ")
    while True:
        await sub_client.post_wiki(
            title=title, content=content, backgroundColor="#C0C0C0"
        )
        print("-- Created wiki...")

        # -- profile tools --

        # -- raid tools __


async def spam_system_messages(sub_client: amino.AsyncSubClient):
    chat_id = await chats(sub_client=sub_client)
    message = input("-- Message::: ")
    message_type = int(input("-- Message Type::: "))
    while True:
        print("-- Spamming...")
        await gather(
            *[
                create_task(sub_client.send_message(chat_id, message, message_type))
                for _ in range(2500)
            ]
        )


async def send_system_message(sub_client: amino.AsyncSubClient):
    chat_id = await chats(sub_client=sub_client)
    message_type = int(input("-- Message Type::: "))
    while True:
        message = input("-- Message::: ")
        await sub_client.send_message(
            chatId=chat_id, message=message, messageType=message_type
        )
        print("-- Message is sent...")


async def join_leave(sub_client: amino.AsyncSubClient, chat_id: str):
    await sub_client.leave_chat(chatId=chat_id)
    await sub_client.join_chat(chatId=chat_id)


async def spam_with_join_leave(sub_client: amino.AsyncSubClient):
    chat_id = await chats(sub_client=sub_client)
    while True:
        print("-- spamming with join and leave...")
        await gather(
            *[create_task(join_leave(sub_client, chat_id)) for _ in range(2500)]
        )


async def join_active_chats(sub_client: amino.AsyncSubClient):
    public_chats = await sub_client.get_public_chat_threads(size=100).chatId
    print("-- Joining into public chats...")
    await gather(
        *[create_task(sub_client.join_chat(chat_id)) for chat_id in public_chats]
    )

    # -- raid tools --


    # -- main function --

async def main():
    await auth()
    sub_client = await amino.AsyncSubClient(
        comId=await communities(), profile=client.profile
    )
    print(tabulate(menu_configs.main_menu, tablefmt="psql"))
    select = int(input("-- Select::: "))

    if select == 1:
        print(tabulate(menu_configs.spam_tools_menu, tablefmt="psql"))
        select = int(input("-- Select::: "))

        if select == 1:
            await spam_bot(sub_client=sub_client)

        elif select == 2:
            await wiki_spam_bo(sub_client=sub_client)

        elif select == 3:
            await wall_spam_bot(sub_client=sub_client)

        elif select == 4:
            await blog_spam_bot(sub_client=sub_client)

    elif select == 2:
        print(tabulate(menu_configs.chat_tools_menu, tablefmt="psql"))
        select = int(input("-- Select::: "))

        if select == 1:
            await chat_id_finder(sub_client=sub_client)

        elif select == 2:
            await crash_chat_description(sub_client=sub_client)

        elif select == 3:
            await transfer_fake_coins(sub_client=sub_client)

    elif select == 3:
        print(tabulate(menu_configs.activity_tools_menu, tablefmt="psql"))
        select = int(input("-- Select::: "))

        if select == 1:
            await chat_invite_bot(sub_client=sub_client)

        elif select == 2:
            await like_bot(sub_client=sub_client)

        elif select == 3:
            await follow_bot(sub_client=sub_client)

        elif select == 4:
            await unfollow_bot(sub_client=sub_client)

    elif select == 4:
        print(tabulate(menu_configs.profile_tools_menu, tablefmt="psql"))
        select = int(input("-- Select::: "))

        if select == 1:
            await blogs_spam(sub_client=sub_client)

        elif select == 2:
            await wiki_spam(sub_client=sub_client)

    elif select == 5:
        print(tabulate(menu_configs.raid_tools_menu, tablefmt="psql"))
        select = int(input("-- Select::: "))

        if select == 1:
            await spam_system_messages(sub_client=sub_client)

        elif select == 2:
            await send_system_message(sub_client=sub_client)

        elif select == 3:
            await spam_with_join_leave(sub_client=sub_client)

        elif select == 4:
            await join_active_chats(sub_client=sub_client)

    elif select == 0:
        exit()

			# End...
