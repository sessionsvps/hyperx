from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
import os
import json
import asyncio

# async def getListOfGroups(client):
#     try:
#         dialogs = await client.get_dialogs()
#         groups_info = []
#         print("Lista de grupos y canales disponibles:")
#         for index, dialog in enumerate(dialogs, start=1):
#             if dialog.is_group or dialog.is_channel:
#                 entity = await client.get_entity(dialog.id)
#                 can_send_messages = entity.default_banned_rights is None or not entity.default_banned_rights.send_messages
#                 if can_send_messages:
#                     group_info = {'group_id': dialog.id, 'group_name': dialog.title}
#                     groups_info.append(group_info)
#                     # Imprimir la lista de grupos enumerada
#                     print(f"{index}. Nombre: {dialog.title}, ID: {dialog.id}")
#         return groups_info
#     except Exception as e:
#         print(e)
#         return []

async def getListOfGroups(client):
    try:
        dialogs = await client.get_dialogs()
        groups_info = []
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                entity = await client.get_entity(dialog.id)
                can_send_messages = entity.default_banned_rights is None or not entity.default_banned_rights.send_messages
                if can_send_messages:
                    group_info = {'group_id': dialog.id, 'group_name': dialog.title}
                    groups_info.append(group_info)

        return groups_info
    except Exception as e:
        print(e)
        return []

async def getMessagesFromGroup(client, group_id):
    try:
        all_messages = []
        async for message in client.iter_messages(group_id):
            try:
                all_messages.append(message)
            except:
                pass
        return all_messages
    except Exception as e:
        print(e)
        return []
    

async def logUserBot():
    load_dotenv()
    api_id = int(29622820)
    api_hash = "f0786ca5671655b8ffcbd1dffaef9e21"
    phone_number = "51964137264"
    session_name = "bot_spammer"
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Ingrese el código de verificación: '))
    await client.send_message("@spmhyperx", f'<b>Bot encendido</b>', parse_mode="HTML")
    spammer_group = int("-4507228542")
    spammer_group2 = int("-4507228542")

    # Lista de IDs de grupos/canales a los que no quieres enviar mensajes
    excluded_group_ids = [-4507228542,-1002368185878,-1002001880141,-1001737351681,-1001859082953,-1001733869168,-1001713225856,-1001829996546,-1001580673964,-1002018025154,-1001907073788,-1001873690567,-1002089490611,-4191583507]  # Reemplaza con los IDs de los grupos a excluir
    special_group_ids = [-1001867739320,-1001617010310,-1002074331354,-1002221235561,-1001789640951,-1002125807620,-1001760634472,-1001724620371]  # Reemplaza con los IDs de los grupos especiales

    while True:
        groups_info = await getListOfGroups(client)
        messages_list = await getMessagesFromGroup(client, spammer_group)
        special_messages_list = await getMessagesFromGroup(client, spammer_group2)  # MENSAJES PARA GRUPOS DONDE NO DEJAN MANDAR TEXTO LARGO O PALABRAS ESPECIALES
            
        try:
            await client.send_message("@spmhyperx", f"<b>CANTIDAD DE MENSAJES CONSEGUIDOS PARA PUBLICAR</b> <code>{len(messages_list)-1}</code>", parse_mode="HTML")
        except:
            pass
            
        try:
            for i in groups_info:
                if i['group_id'] not in excluded_group_ids:  # Compara por group_id en lugar de group_name

                    if i['group_id'] in special_group_ids:  # Compara por group_id en lugar de group_name
                        j = 0
                        for message_spam in special_messages_list:
                            j += 1
                            resultado = True
                            try:
                                await client.forward_messages(i["group_id"], message_spam)
                            except Exception as error:
                                await client.send_message("@spmhyperx", f'<b>Error enviando mensajes a {i["group_id"]}</b> - <code>{i["group_name"]}<code>\nCausa:{error}', parse_mode="HTML")
                                resultado = False
                            if resultado:
                                await client.send_message("@spmhyperx", f'<b>Mensaje enviado a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")  
                            await asyncio.sleep(50)
                            if j == 2: break
                    else:
                        j = 0
                        for message_spam in messages_list:
                            j += 1
                            resultado = True
                            try:
                                await client.forward_messages(i["group_id"], message_spam)
                            except Exception as error:
                                await client.send_message("@spmhyperx", f'<b>Error enviando mensajes a {i["group_id"]}</b> - <code>{i["group_name"]}<code>\nCausa:{error}', parse_mode="HTML")
                                resultado = False
                            if resultado:
                                await client.send_message("@spmhyperx", f'<b>Mensaje enviado a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")  
                            await asyncio.sleep(10)
                            if j == 2: break
            await client.send_message("@spmhyperx", f'<b>RONDA ACABADA</b>', parse_mode="HTML")
            await asyncio.sleep(100) 
        except:
            pass

if __name__ == "__main__":
    asyncio.run(logUserBot())