import telebot
import requests

import base64

from datetime import datetime
from datetime import timedelta
import threading
from time import sleep
from telebot import types
from pprint import pprint
from pymongo import MongoClient

# Авторизация
autorizationforAPI = {"Password"}

headersforAPI1 = {"password"}

headersforAPI2 = {"password"}

autorizationforwork = {
    'Authorization': ''}

headersforwork = {'Content-Type': 'application/json',
                  'Authorization': ''}

bot = telebot.TeleBot('861638739:AAGO3Tt7OaedDXcpVUww77LOuLgBgn6SOUw',threaded=False)

Numberphone = ""
family_name = ""
name = ""
given_name = ""
distributor_id = ""
userID = ""
lastname = ""
firstname = ""
newphone = ""
text_message = ""
chat = ""
orders = []
copy_alltext = {}
Debts = []
OverdueDebts = []
AllSumaDebts = []
AllOverdueDebts = []

array_of_dicts = []
ordersname = []
ID = ''
IDforPhoto = ''
name = ''
vendor = ''
text = ''
end_string = ''
one = ''
IDsroutes = []
Namereponsibleroutes = []
ListNamereponsibleroutes = []
ListIDresponsibleroutes = []
IDresponsibs = []
Nameresponsibs = ''
alltext = []
today = ""
datainjson = ""
answearIDforTask = ""
alltext3 = ""
alltext4 = ""
data = ""
sumaI1 = 0
sumaI2 = 0
datas = {}
wanted_keys = ["given_name", "family_name", "distributor_id", "middle_name", "name"]
nameformat = ""
namecategory = ""
wanted_keys_for_orders = ["name", "sum"]

InfoAboutUser = {
    'distributor_id': '',
    'given_name': '',
    'family_name': '',
    'middle_name': '',
    'name': '',
    'id': '',
    'telegram_contact':
        {'phone_number': '', 'first_name': '', 'last_name': '', 'user_id': ''}

}
TTsearch = {
    "searchString": ""
}
infobyTT = {
    "searchString": ""
}
createtask = {
    "tradeOutletId": "",
    "responsibleId": "",
    "statusId": "",
    "name": "",
    "description": "",
    "dateTill": ""
}
photoforTask = {
    "name": ".jpg",
    "content": ""
}

photoforTT = {
    "typeId": "",
    "geoCoordinate": {"latitude": 1.1,
                      "longitude": 1.1},
    "content": ""
}

setinvoices = {

    "routeIds": "",
    "officeIds": "",
    "salesDepartmentIds": "",

    "dateFrom": "",
    "dateTill": ""

}

afterworkkeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
infoTT = types.InlineKeyboardButton(text="Информация о торговую точку", callback_data='information')
task = types.InlineKeyboardButton(text="Создать задачу", callback_data="createtask")
photo = types.InlineKeyboardButton(text="Загрузить фото", callback_data="loadphoto")
gm = types.InlineKeyboardButton(text="Главное меню", callback_data="GM")

afterworkkeyboard.add(infoTT, task, photo, gm)

try:
    Client = MongoClient()
    print(Client)
except:
    print("could not to connect")


def listening(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print("[" + str(cid) + "]: " + m.text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global Numberphone, userID, lastname, firstname, InfoAboutUser
    db = Client.TelegramUsers

    coll = db.Users
    ID_user = message.from_user.id
    print(ID_user)

    searchdata = {"telegram_contact.phone_number": ID_user}

    search = coll.find_one(searchdata)
    print(search)
    for key in InfoAboutUser:
        InfoAboutUser['distributor_id'] = ""
        InfoAboutUser['given_name'] = ""
        InfoAboutUser['family_name'] = ""
        InfoAboutUser['middle_name'] = ""
        InfoAboutUser['name'] = ""
        InfoAboutUser['id'] = ""
        InfoAboutUser['telegram_contact']['phone_number'] = ""
        InfoAboutUser['telegram_contact']['first_name'] = ""
        InfoAboutUser['telegram_contact']['last_name'] = ""
        InfoAboutUser['telegram_contact']['user_id'] = ""

    pprint(InfoAboutUser)

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    contact = telebot.types.KeyboardButton("Отправить контакт", request_contact=True)
    keyboard.add(contact)

    InfoAboutUser['telegram_contact']['user_id'] = message.from_user.id

    InfoAboutUser['telegram_contact']['last_name'] = message.from_user.last_name
    InfoAboutUser['telegram_contact']['first_name'] = message.from_user.first_name
    firstname = message.from_user.first_name
    pprint(InfoAboutUser)
    bot.send_chat_action(message.chat.id, 'typing')

    bot.send_message(message.chat.id, "Отправте свой контакт", reply_markup=keyboard)
    bot.register_next_step_handler(message, contact_handler)


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    global Numberphone, family_name, name, given_name, distributor_id, newphone, firstname, datas, wanted_keys, InfoAboutUser

    Numberphone = message.contact.phone_number
    newphone = Numberphone.replace("+", "")

    InfoAboutUser['telegram_contact']['phone_number'] = newphone
    print(Numberphone)
    print(newphone)

    try:

        url = '' + newphone
        autorizationtoData = requests.get(url,
                                          headers=headersforAPI1)
        print(autorizationtoData)

        db = Client.TelegramUsers
        Users = db.Users

        getID = autorizationtoData.json()  # .get('id',[])
        getclaims = autorizationtoData.json().get('claims')

        for claim in getclaims:
            if claim['claimType'] in wanted_keys:
                datas[claim['claimType']] = claim['claimValue']

        print(datas)

        if datas.get('middle_name'):
            InfoAboutUser['middle_name'] = datas.get('middle_name')


        else:
            print(123)

        InfoAboutUser['name'] = datas.get('name')

        autorizationforAPI['user_id'] = getID['id']
        InfoAboutUser['id'] = getID['id']

        distributor_id = getID['claims'][2]['claimValue']
        InfoAboutUser['distributor_id'] = distributor_id

        given_name = getID['claims'][0]['claimValue']

        InfoAboutUser['given_name'] = given_name

        family_name = getID['claims'][1]['claimValue']
        InfoAboutUser['family_name'] = family_name

        removekeyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "Добро пожаловать " + str(firstname) + ' ☺ ' + '\n' + "Меня зовут Диди 🤖." +
                         "Чтобы начать роботать с торговыми точками, нажмите на эту команду: /work",
                         reply_markup=removekeyboard)

        autori = requests.post('', data=autorizationforAPI,
                               headers=headersforAPI2)
        print(autori)

        access_token = autori.json().get('access_token', [])

        headersforwork['Authorization'] = 'Bearer ' + access_token
        headersforwork['Authorization'] = 'Bearer ' + access_token
        autorizationforwork['Authorization'] = 'Bearer ' + access_token

        # Закгрузка в БД
        Users.insert_one(InfoAboutUser)

    except:
        try:
            db = Client.TelegramUsers

            coll = db.Users

            searchdata = {"telegram_contact.phone_number": newphone}

            search = coll.find_one(searchdata)
            if search:
                autorizationforAPI['user_id'] = search.get('id')

            else:
                print('not found')

            if autorizationforAPI['user_id']:
                removekeyboard = telebot.types.ReplyKeyboardRemove(selective=False)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id,
                                 "Добро пожаловать " + str(firstname) + ' ☺ ' + '\n' + "Меня зовут Диди 🤖." +
                                 "Что бы начать роботать с торговыми точками нажмите на эту команду /work",
                                 reply_markup=removekeyboard)

                autori = requests.post('', data=autorizationforAPI,
                                       headers=headersforAPI2)
                print(autori)

                access_token = autori.json().get('access_token', [])

                headersforwork['Authorization'] = 'Bearer ' + access_token
                headersforwork['Authorization'] = 'Bearer ' + access_token
                autorizationforwork['Authorization'] = 'Bearer ' + access_token


            else:
                removekeyboard = telebot.types.ReplyKeyboardRemove(selective=False)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, "Я тебя не знаю", reply_markup=removekeyboard)

        except:
            print(123)


@bot.message_handler(commands=["work"])
def start_work(message):
    global newphone, Numberphone, ListIDresponsibleroutes, ListNamereponsibleroutes, ordersname, sumaI1, ID, IDresponsibs, AllOverdueDebts, AllSumaDebts, ordersname, Debts, OverdueDebts, \
        nameformat, namecategory

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        IDwithoutautori = message.from_user.id

        db = Client.TelegramUsers

        coll = db.Users

        searchdata = {"telegram_contact.user_id": IDwithoutautori}
        print(searchdata)

        search = coll.find_one(searchdata)

        autorizationforAPI['user_id'] = search.get('id')
        print(autorizationforAPI)
        autori = requests.post('', data=autorizationforAPI,
                               headers=headersforAPI2)
        print(autori)

        access_token = autori.json().get('access_token', [])

        print(access_token)

        headersforwork['Authorization'] = 'Bearer ' + access_token
        headersforwork['Authorization'] = 'Bearer ' + access_token
        autorizationforwork['Authorization'] = 'Bearer ' + access_token

    except:
        print('not found')

    if autorizationforAPI['user_id']:

        del ListIDresponsibleroutes[:]
        del ListNamereponsibleroutes[:]
        del ordersname[:]
        del IDresponsibs[:]
        sumaI1 = 0
        ID = ""
        del AllOverdueDebts[:]
        del AllSumaDebts[:]
        del ordersname[:]
        del OverdueDebts[:]
        del Debts[:]
        nameformat = ""
        namecategory = ""
        del orders[:]

        print(ListNamereponsibleroutes)
        print(ListIDresponsibleroutes)
        print(ordersname)
        print("ID= " + ID)

        bot.send_message(message.chat.id,
                         "Введите название Торговой точки, часть названия Торг.точки(пример 'маг'), адрес торг точки или просто символ(если он есть в название торг.точки(Пример '№')).")
        bot.register_next_step_handler(message, get_search)

    else:
        bot.send_message(message.chat.id,
                         "Сначала надо авторизироваться с помощю команды /start. После чего ты сможешь начать роботать")


def get_search(message):
    global name, text, vendor, sumaI1, ListIDresponsibleroutes, ListNamereponsibleroutes, IDresponsibs, one

    bot.send_chat_action(message.chat.id, 'typing')

    TTsearch["searchString"] = message.text
    pprint(TTsearch)

    url = ''
    data = requests.post(url, json=TTsearch, headers=headersforwork)
    print(data)

    text = data.json().get('data', [])

    for i in range(len(text)):
        name = text[i]['name']
        # vendor = text[i]['vendorId']
        address = text[i]['location']['addressLine']
        pprint(name)

        sumaI1 += i

    print(sumaI1)

    selectKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    if text:
        if sumaI1 == 0:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one)


        elif sumaI1 == 1:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two)

        elif sumaI1 == 3:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")
                three = types.InlineKeyboardButton(
                    text=str(text[2]['name']) + "  " + str(text[2]['location']['addressLine']),
                    callback_data="three")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two, three)

        elif sumaI1 == 6:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")
                three = types.InlineKeyboardButton(
                    text=str(text[2]['name']) + "  " + str(text[2]['location']['addressLine']),
                    callback_data="three")
                four = types.InlineKeyboardButton(
                    text=str(text[3]['name']) + "  " + str(text[3]['location']['addressLine']),
                    callback_data="four")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two, three, four)

        elif sumaI1 == 10:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")
                three = types.InlineKeyboardButton(
                    text=str(text[2]['name']) + "  " + str(text[2]['location']['addressLine']),
                    callback_data="three")
                four = types.InlineKeyboardButton(
                    text=str(text[3]['name']) + "  " + str(text[3]['location']['addressLine']),
                    callback_data="four")
                five = types.InlineKeyboardButton(
                    text=str(text[4]['name']) + "  " + str(text[4]['location']['addressLine']),
                    callback_data="five")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two, three, four, five)



        elif sumaI1 == 15:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")
                three = types.InlineKeyboardButton(
                    text=str(text[2]['name']) + "  " + str(text[2]['location']['addressLine']),
                    callback_data="three")
                four = types.InlineKeyboardButton(
                    text=str(text[3]['name']) + "  " + str(text[3]['location']['addressLine']),
                    callback_data="four")
                five = types.InlineKeyboardButton(
                    text=str(text[4]['name']) + "  " + str(text[4]['location']['addressLine']),
                    callback_data="five")
                six = types.InlineKeyboardButton(
                    text=str(text[5]['name']) + "  " + str(text[5]['location']['addressLine']),
                    callback_data="six")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two, three, four, five, six)

        elif sumaI1 == 21:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")
                three = types.InlineKeyboardButton(
                    text=str(text[2]['name']) + "  " + str(text[2]['location']['addressLine']),
                    callback_data="three")
                four = types.InlineKeyboardButton(
                    text=str(text[3]['name']) + "  " + str(text[3]['location']['addressLine']),
                    callback_data="four")
                five = types.InlineKeyboardButton(
                    text=str(text[4]['name']) + "  " + str(text[4]['location']['addressLine']),
                    callback_data="five")
                six = types.InlineKeyboardButton(
                    text=str(text[5]['name']) + "  " + str(text[5]['location']['addressLine']),
                    callback_data="six")
                seven = types.InlineKeyboardButton(
                    text=str(text[6]['name']) + "  " + str(text[6]['location']['addressLine']),
                    callback_data="seven")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two, three, four, five, six, seven)

        elif sumaI1 == 28:
            for i in range(len(text)):
                one = types.InlineKeyboardButton(
                    text=str(text[0]['name']) + "  " + str(text[0]['location']['addressLine']), callback_data="first")
                two = types.InlineKeyboardButton(
                    text=str(text[1]['name']) + "  " + str(text[1]['location']['addressLine']), callback_data="second")
                three = types.InlineKeyboardButton(
                    text=str(text[2]['name']) + "  " + str(text[2]['location']['addressLine']),
                    callback_data="three")
                four = types.InlineKeyboardButton(
                    text=str(text[3]['name']) + "  " + str(text[3]['location']['addressLine']),
                    callback_data="four")
                five = types.InlineKeyboardButton(
                    text=str(text[4]['name']) + "  " + str(text[4]['location']['addressLine']),
                    callback_data="five")
                six = types.InlineKeyboardButton(
                    text=str(text[5]['name']) + "  " + str(text[5]['location']['addressLine']),
                    callback_data="six")
                seven = types.InlineKeyboardButton(
                    text=str(text[6]['name']) + "  " + str(text[6]['location']['addressLine']),
                    callback_data="seven")
                eight = types.InlineKeyboardButton(
                    text=str(text[7]['name']) + "  " + str(text[7]['location']['addressLine']),
                    callback_data="eight")

            sumaI1 = 0
            print(sumaI1)
            selectKeyboard.add(one, two, three, four, five, six, seven, eight)

        bot.send_message(message.chat.id, "Выберите Торговую точку:  ",
                         reply_markup=selectKeyboard)

    else:
        bot.send_message(message.chat.id, "Ничего не найдено")


def get_nameTask(message):
    global ID
    createtask["name"] = message.text

    print(createtask["name"])
    bot.send_message(message.from_user.id, "Введите описания к задаче ✍")
    bot.register_next_step_handler(message, get_description)


def get_description(message):
    createtask["description"] = message.text
    print(createtask["description"])
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    oneweek = types.InlineKeyboardButton(text="Через неделю", callback_data='afteroneweek')
    twoweek = types.InlineKeyboardButton(text="Через две недели", callback_data='aftertwoweek')
    onemonth = types.InlineKeyboardButton(text="Через месяц", callback_data='aftermonth')
    keyboard.add(oneweek, twoweek, onemonth)

    bot.send_message(message.chat.id, "Выберите срок действия задачи", reply_markup=keyboard)


def photo(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton(text="Да", callback_data='key_yes')
    no = types.InlineKeyboardButton(text="Нет", callback_data='key_no')

    keyboard.add(yes, no)

    bot.send_message(message.chat.id, "Добавить фото к задаче?", reply_markup=keyboard)


def get_TypeID(message):
    global alltext4, nameTypeID
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_chat_action(message.chat.id, 'typing')

    if message.text == "Вход в ТТ":

        for i in range(len(alltext4)):
            IDtype = alltext4[0]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)




    elif message.text == "Витрина":

        for i in range(len(alltext4)):
            IDtype = alltext4[1]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    elif message.text == "тест2":

        for i in range(len(alltext4)):
            IDtype = alltext4[2]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    elif message.text == "Фото продавщицы":

        for i in range(len(alltext4)):
            IDtype = alltext4[3]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    elif message.text == "Акция":

        for i in range(len(alltext4)):
            IDtype = alltext4[4]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    elif message.text == "Фото в магазине":

        for i in range(len(alltext4)):
            IDtype = alltext4[5]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    elif message.text == "Оборудование":

        for i in range(len(alltext4)):
            IDtype = alltext4[6]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    elif message.text == "Возврат":

        for i in range(len(alltext4)):
            IDtype = alltext4[7]['id']

            photoforTT["typeId"] = IDtype

        print(IDtype)

    bot.register_next_step_handler(bot.send_message(message.chat.id, "Отправте фотографию", reply_markup=markup),
                                   get_photoTT)


def get_photoTT(message):
    global ID
    bot.send_chat_action(message.chat.id, 'typing')
    file = message.photo[-1]
    file = bot.get_file(file.file_id)
    photo_byte = bot.download_file(file.file_path)

    end_string = base64.b64encode(photo_byte)

    photoforTT["content"] = end_string.decode('utf-8')
    print(photoforTT["content"])

    url = '{' + ID + '}'
    data = requests.post(url, json=photoforTT, headers=headersforwork)
    print(data)
    pprint(data.text)
    text = data.json().get('id', [])

    if text:
        bot.send_message(message.chat.id, "Фотография успешно отправлена ☑", reply_markup=afterworkkeyboard)

    else:
        bot.send_message(message.chat.id, "Упссс, что-то пошло не так. Попробуйте снова",
                         reply_markup=afterworkkeyboard)


def get_photoTask(message):
    global answearIDforTask
    bot.send_chat_action(message.chat.id, 'typing')
    file = message.photo[-1]
    file = bot.get_file(file.file_id)
    photo_byte = bot.download_file(file.file_path)

    end_string = base64.b64encode(photo_byte)

    photoforTask["content"] = end_string.decode('utf-8')
    print(photoforTask["content"])

    url = '{' + answearIDforTask + '}'
    data = requests.post(url, json=photoforTask, headers=headersforwork)
    print(data)
    pprint(data.text)

    text = data.json().get('id', [])
    answearIDforTaskPhoto = text
    print(answearIDforTaskPhoto)

    if answearIDforTaskPhoto:
        bot.send_message(message.chat.id, "Задача успешно создана ☑", reply_markup=afterworkkeyboard)

    else:
        bot.send_message(message.chat.id, "Упссс, что-то пошло не так. Попробуйте снова",
                         reply_markup=afterworkkeyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global name, vendor, text, ID, today, datainjson, IDresponsibs, Nameresponsibs, alltext3, answearIDforTask, alltext4, \
        alltext, ListNamereponsibleroutes, Namereponsibleroutes, IDsroutes, nameTypeID, ListIDresponsibleroutes, sumaI2, answerListwithclear, \
        sumaDebts, sumaOverdueDebts, OverdueDebts, Debts, AllOverdueDebts, AllSumaDebts, ListOrders, GeneralListbyOrdersDebtsAndOverdueDebts, sumaI1, \
        nameformat, namecategory, orders

    if call.data == 'information':
        if ID:

            bot.send_message(call.message.chat.id, "Всего несколько секунд и информацию покажу на экране  ) 🔎 ")

            # Инфо по ТТ
            pprint(infobyTT)
            url = ''
            data = requests.post(url, json=infobyTT, headers=headersforwork)

            print(data)

            alltext = data.json().get('data')





            for i in range(len(alltext)):
                bot.send_chat_action(call.message.chat.id, 'typing')
                namecategory = alltext[i]['category']['name']
                nameformat = alltext[i]['format']['name']


                nameTT = alltext[i]['name']
                location = alltext[i]['location']['addressLine']

            bot.send_message(call.message.chat.id, "Названия:  " + name + '\n' + "Адрес:  " + location)

            for block in alltext:
                for relationship in block['relationships']:

                    if relationship['relationship']['debts'] and relationship['relationship']['overdueDebts'] != []:
                        orders.append({
                            'name': relationship['relationship']['name'],
                            'sum_debts': relationship['relationship']['debts'][0]['sum'],
                            'sum_overdue': relationship['relationship']['overdueDebts'][0]['sum']
                        })

                    else:
                        orders.append({
                            'name': relationship['relationship']['name'],
                            'sum_debts': 'Нету инфо',
                            'sum_overdue': 'Нету инфо'
                        })









            print(orders)
            for i in range(len(orders)):
                bot.send_chat_action(call.message.chat.id, 'typing')
                AllSumaDebts.append(orders[i]['sum_debts'])
                AllOverdueDebts.append(orders[i]['sum_overdue'])
                ordersname.append(orders[i]['name'])




            bot.send_message(call.message.chat.id,"Договора:" + '\n' + str(
                                         ' \n'.join('  '.join([w, str(n1), str(n2)]) for w, n1, n2 in zip(ordersname, AllSumaDebts, AllOverdueDebts))))

            bot.send_message(call.message.chat.id,"Долги по каждому договору ="+str(AllSumaDebts)+'\n'
                             +"Просроченные долги по каждому договору ="+str(AllOverdueDebts))






            ListIDresponsibleroutes = [routeDict['id'] for routeDict in alltext[0]['routes']]






            print(ListIDresponsibleroutes)
            print(ListNamereponsibleroutes)
            for i in range(len(ListIDresponsibleroutes)):
                bot.send_chat_action(call.message.chat.id, 'typing')
                IDRT = ListIDresponsibleroutes[i]

                url2 = ''
                data2 = requests.get(url2, headers=autorizationforwork)
                print(data2)

                alltext2 = data2.json().get('responsible', [])
                pprint(alltext2)

                ListNamereponsibleroutes.append(alltext2['fullName'])
                IDresponsibs.append(alltext2['id'])

            print(IDresponsibs)

            print(ListNamereponsibleroutes)

            bot.send_chat_action(call.message.chat.id, 'typing')

            bot.send_message(call.message.chat.id, "Все ответственны за эту торговую точку:" + '\n' + str(
                '\n'.join(ListNamereponsibleroutes)))

            bot.send_chat_action(call.message.chat.id, 'typing')
            bot.send_message(call.message.chat.id,
                             "Категория: " + str(namecategory) + '\n' + "Формат: " + str(nameformat),
                             reply_markup=afterworkkeyboard)

        else:
            bot.send_message(call.message.chat.id, "Не возможно получить информацию.")




    elif call.data == 'createtask':
        if ID:
            if ListNamereponsibleroutes:
                bot.send_chat_action(call.message.chat.id, 'typing')

                for i in range(len(ListNamereponsibleroutes)):
                    sumaI2 += i
                    print(sumaI2)

                markup = types.InlineKeyboardMarkup(row_width=2)

                if sumaI2 == 0:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one)

                elif sumaI2 == 1:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two)

                elif sumaI2 == 3:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three)

                elif sumaI2 == 6:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four)

                elif sumaI2 == 10:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five)

                elif sumaI2 == 15:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six)

                elif sumaI2 == 21:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven)

                elif sumaI2 == 28:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight)

                elif sumaI2 == 36:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]), callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")
                        nine = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[8]),
                            callback_data="eightTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight, nine)

                elif sumaI2 == 45:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")
                        nine = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[8]),
                            callback_data="nineTT")
                        ten = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[9]),
                            callback_data="tenTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight, nine, ten)

                elif sumaI2 == 55:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")
                        nine = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[8]),
                            callback_data="nineTT")
                        ten = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[9]),
                            callback_data="tenTT")

                        eleven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[10]),
                            callback_data="elevenTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight, nine, ten, eleven)

                elif sumaI2 == 66:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")
                        nine = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[8]),
                            callback_data="nineTT")
                        ten = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[9]),
                            callback_data="tenTT")

                        eleven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[10]),
                            callback_data="elevenTT")

                        twelve = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[11]),
                            callback_data="twelveTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve)

                elif sumaI2 == 78:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")
                        nine = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[8]),
                            callback_data="nineTT")
                        ten = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[9]),
                            callback_data="tenTT")

                        eleven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[10]),
                            callback_data="elevenTT")

                        twelve = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[11]),
                            callback_data="twelveTT")

                        Thirteen = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[12]),
                            callback_data="thirteenTT")

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, Thirteen)

                elif sumaI2 == 91:
                    for i in range(len(ListNamereponsibleroutes)):
                        one = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[0]),
                            callback_data="firstTT")
                        two = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[1]),
                            callback_data="secondTT")
                        three = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[2]),
                            callback_data="threeTT")
                        four = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[3]),
                            callback_data="fourTT")
                        five = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[4]),
                            callback_data="fiveTT")
                        six = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[5]),
                            callback_data="sixTT")
                        seven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[6]),
                            callback_data="sevenTT")
                        eight = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[7]),
                            callback_data="eightTT")
                        nine = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[8]),
                            callback_data="nineTT")
                        ten = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[9]),
                            callback_data="tenTT")

                        eleven = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[10]),
                            callback_data="elevenTT")

                        twelve = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[11]),
                            callback_data="twelveTT")

                        Thirteen = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[12]),
                            callback_data="thirteenTT")

                        fourteen = types.InlineKeyboardButton(
                            text=str(ListNamereponsibleroutes[13]),
                            callback_data="fourteenTT"
                        )

                    sumaI2 = 0
                    print(sumaI2)
                    markup.add(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, Thirteen,
                               fourteen)

                if ListNamereponsibleroutes:

                    bot.send_message(call.message.chat.id,
                                     "Выберите исполнителя задачи за которым будет закреплена задача",
                                     reply_markup=markup),

                else:
                    bot.send_message(call.message.chat.id, "Пусто")
            else:
                bot.send_message(call.message.chat.id,
                                 "Сначала нужно получить информацию про торг.точку, а после этого создавать задачу")

        else:
            bot.send_message(call.message.chat.id, "Не возможно начать создания задачи.")








    elif call.data == 'afteroneweek':
        bot.send_chat_action(call.message.chat.id, 'typing')

        today = datetime.today()
        deltaData = timedelta(days=7)
        new_dataforweek = today + deltaData
        datainjson = new_dataforweek.isoformat() + "Z"
        print(datainjson)

        createtask["dateTill"] = datainjson
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton(text="Да", callback_data='key_yes')
        no = types.InlineKeyboardButton(text="Нет", callback_data='key_no')

        keyboard.add(yes, no)

        bot.send_message(call.message.chat.id, "Добавить фото?", reply_markup=keyboard),



    elif call.data == 'aftertwoweek':
        bot.send_chat_action(call.message.chat.id, 'typing')

        today = datetime.today()
        deltaData = timedelta(days=14)
        new_dataforweek = today + deltaData
        datainjson = new_dataforweek.isoformat() + "Z"
        print(datainjson)

        createtask["dateTill"] = datainjson
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton(text="Да", callback_data='key_yes')
        no = types.InlineKeyboardButton(text="Нет", callback_data='key_no')

        keyboard.add(yes, no)

        bot.send_message(call.message.chat.id, "Добавить фото?", reply_markup=keyboard)

    elif call.data == 'aftermonth':
        bot.send_chat_action(call.message.chat.id, 'typing')

        today = datetime.today()
        deltaData = timedelta(days=29)
        new_dataforweek = today + deltaData
        datainjson = new_dataforweek.isoformat() + "Z"
        print(datainjson)

        createtask["dateTill"] = datainjson
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton(text="Да", callback_data='key_yes')
        no = types.InlineKeyboardButton(text="Нет", callback_data='key_no')

        keyboard.add(yes, no)

        bot.send_message(call.message.chat.id, "Добавить фото?", reply_markup=keyboard)

    elif call.data == 'key_no':
        bot.send_chat_action(call.message.chat.id, 'typing')
        url = 'https://sfa-api.ddapp.biz/api/tasks'
        data = requests.post(url, json=createtask, headers=headersforwork)
        print(data)
        pprint(data.text)

        text = data.json().get('id', [])
        answearIDforTask = text
        print(answearIDforTask)
        if answearIDforTask:
            bot.send_message(call.message.chat.id, "Успешно создано", reply_markup=afterworkkeyboard)

        else:
            bot.send_message(call.message.chat.id, "Упссс, что-то пошло не так. Попробуйте снова",
                             reply_markup=afterworkkeyboard)

    elif call.data == 'key_yes':
        bot.send_chat_action(call.message.chat.id, 'typing')
        url = 'https://sfa-api.ddapp.biz/api/tasks'
        data = requests.post(url, json=createtask, headers=headersforwork)
        print(data)
        pprint(data.text)

        text = data.json().get('id', [])
        answearIDforTask = text
        print(answearIDforTask)
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, "Отправьте фотографию"), get_photoTask)



    elif call.data == 'loadphoto':
        if ID:
            bot.send_chat_action(call.message.chat.id, 'typing')
            url4 = ''
            data = requests.get(url4, headers=autorizationforwork)
            print(data)
            # pprint(data.text)
            alltext4 = data.json().get('data', [])
            # print(text)

            for i in range(len(alltext4)):
                TypeID = alltext4[i]['id']
                nameTypeID = alltext4[i]['name']

                print(nameTypeID)

            selectmarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)

            for i in range(len(alltext4)):
                selectmarkup.add(types.KeyboardButton(text=str(alltext4[i]['name'])))

            bot.register_next_step_handler(
                bot.send_message(call.message.chat.id, "Выбирите тип для фотографий из предложенного ",
                                 reply_markup=selectmarkup), get_TypeID)

        else:
            bot.send_chat_action(call.message.chat.id, 'typing')
            bot.send_message(call.message.chat.id, "Невозможно загрузить фотографию торг.точки")










    # Торг.точки

    elif call.data == "first":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[0]['id']
            name = text[0]['name']
            infobyTT["searchString"] = text[0]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)
        print(name)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)



    elif call.data == "second":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[1]['id']
            name = text[1]['name']
        infobyTT["searchString"] = text[1]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)

    elif call.data == "three":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[2]['id']
            name = text[2]['name']

        infobyTT["searchString"] = text[2]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)

    elif call.data == "four":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[3]['id']
            name = text[3]['name']

        infobyTT["searchString"] = text[3]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)

    elif call.data == "five":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[4]['id']
            name = text[4]['name']

        infobyTT["searchString"] = text[4]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)

    elif call.data == "six":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[5]['id']
            name = text[5]['name']

        infobyTT["searchString"] = text[5]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)

    elif call.data == "seven":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[6]['id']
            name = text[6]['name']

        infobyTT["searchString"] = text[6]['location']['addressLine']
        createtask["tradeOutletId"] = ID

        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)

    elif call.data == "eight":
        bot.send_chat_action(call.message.chat.id, 'typing')

        for i in range(len(text)):
            ID = text[7]['id']
            name = text[7]['name']

        infobyTT["searchString"] = text[7]['location']['addressLine']
        createtask["tradeOutletId"] = ID
        print(ID)

        bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=afterworkkeyboard)
    # Отвествыные
    elif call.data == "firstTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[0]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "secondTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[1]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "threeTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[2]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "fourTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[3]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "fiveTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[4]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "sixTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[5]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "sevenTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[6]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "eightTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[7]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "nineTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[8]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "tenTT":
        bot.send_chat_action(call.message.chat.id, 'typing')

        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[9]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "elevenTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[10]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "twelveTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[11]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "thirteenTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[12]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "fourteenTT":
        bot.send_chat_action(call.message.chat.id, 'typing')
        if TTsearch:
            for i in range(len(ListIDresponsibleroutes)):
                createtask["responsibleId"] = IDresponsibs[13]

            print(createtask["responsibleId"])

            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите названия задачи ✍"),
                                           get_nameTask)
        else:
            bot.send_message(call.message.chat.id, "Не возможно создать задачу")

    elif call.data == "GM":
        del ListIDresponsibleroutes[:]
        del ListNamereponsibleroutes[:]
        del ordersname[:]
        del IDresponsibs[:]
        sumaI1 = 0
        ID = ""
        del AllOverdueDebts[:]
        del AllSumaDebts[:]
        del ordersname[:]

        print(ListNamereponsibleroutes)
        print(ListIDresponsibleroutes)
        print(ordersname)
        print("ID= " + ID)
        bot.send_message(call.message.chat.id,
                         "Добро пожаловать в главное меню ☺. Если хотите начать роботать с новой торговой точкой, просто нажмите на команду: /work")


while True:
    try:

        pool=threading.Thread(target=bot.polling(none_stop=True,  timeout=50))
        pool=threading.Thread(target=bot.infinity_polling(True))
        pool.start()

        bot.set_update_listener(listening)






    except Exception:
        pass

    except AttributeError:
        pass

    except ReferenceError:
        pass

    except telebot.apihelper.requests.exceptions.ConnectionError:
        pass

    except ConnectionAbortedError:
        pass

    except ConnectionRefusedError:
        pass

    except ConnectionResetError:
        pass

    except RuntimeError:
        pass

    except telebot.apihelper.requests.exceptions.ConnectTimeout:
        pass

    except IndexError:
        pass

    except telebot.apihelper.requests.exceptions.ReadTimeout:
        pass

    except telebot.apihelper.requests.exceptions.RetryError:
        pass

    except telebot.apihelper.requests.exceptions.Timeout:
        pass

    except telebot.apihelper.requests.exceptions.HTTPError:
        pass

    except RecursionError:
        pass



    finally:

        pass
