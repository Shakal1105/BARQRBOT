from pyzbar import pyzbar
from telebot import *
from PIL import Image

class Bot():
    def __init__(self):
        self.admins = [697798016, 897669172]
        self.checker = 0
        self.help = 1
        self.text_writer=""
        self.bot = TeleBot("5554216479:AAETVvLqz9xJPEp_jO0gfx4GyAN_t-IBYFs")
        print("work")

        @self.bot.message_handler(commands=["start"])
        def start(mess):
            self.bot.send_message(mess.chat.id, "work")

        @self.bot.message_handler(commands=["update"])
        def sending_file(mess):
            if mess.from_user.id in self.admins:
                try:
                    self.bot.send_message(mess.chat.id, "CODE==>NAME==>COUNT==>PRICE==>FULL PRICE")
                    self.bot.send_document(mess.chat.id, open(r"db.txt", 'rb'))
                except Exception as e:
                    self.bot.send_message(mess.chat.id, "Ошибка. Файл пустой чтобы бот отправил файл сначала заполните его содержимим")

        @self.bot.message_handler(content_types=["text"])
        def text_hundler(m):
            if m.from_user.id in self.admins:
                print(m.from_user.id)
                if m.text[:3] == "add":
                    self.admins.append(int(m.text[3:]))
                    self.bot.send_message(m.chat.id,'користувач {} отримав права администратора'.format(m.text[3:]))
                elif m.text[:3] == "del":
                    self.admins.remove(int(m.text[3:]))
                    self.bot.send_message(m.chat.id,"користувач {} лишился прав администратора".format(m.text[3:]))
                mid=m.id
                text = m.text
                if self.checker == -1:
                    self.text_writer = text+"@"
                    self.bot.delete_message(m.chat.id, mid)
                    self.bot.send_message(m.chat.id, f"{text}\nВведiть назву товару:")
                    self.old_code="Штрихкод: "+text
                    self.new_id = mid+1
                    self.checker=1
                elif self.checker == 1:
                    self.text_writer = self.text_writer+text+"@"
                    self.bot.delete_message(m.chat.id, mid)
                    self.bot.edit_message_text(chat_id=m.chat.id, message_id=self.new_id, text=f"{self.old_code}\n{text}\nВведiть кількість товару:")
                    self.old_name="Описание: "+text
                    self.checker=2
                elif self.checker == 2:
                    try:
                        text = int(text)
                        if type(text) is int:
                            self.text_writer=self.text_writer+str(text)+"@"
                            self.bot.delete_message(m.chat.id, mid)
                            self.bot.edit_message_text(chat_id=m.chat.id, message_id=self.new_id, text=f"{self.old_code}\n{self.old_name}\nКоличество: {text} шт\nВведiть ціну товару:")
                            self.checker=3
                            self.old_count =str(text)
                    except Exception:
                        self.bot.delete_message(m.chat.id, mid)
                        self.bot.send_message(m.chat.id, "Некоректно введено количество товара используйте цифры")
                        self.checker=2

                elif self.checker == 3:
                    try:
                        text = text.replace(",", ".")
                        text = float(text)
                        if type(text) is float:
                            self.text_writer=self.text_writer+str(text)+"@"+str(float(self.old_count)*text)
                            self.bot.delete_message(m.chat.id, mid)
                            self.bot.edit_message_text(chat_id=m.chat.id, message_id=self.new_id, text=f"{self.old_code}\n{self.old_name}\nКоличество: {self.old_count} шт\nЦіна за шт: {text}\nОбщая цена:{float(self.old_count)*text} грн")
                            self.checker=0
                            time.sleep(1)
                            self.bot.delete_message(m.chat.id, self.new_id)
                            file = open("db.txt", "a")
                            file.write(self.text_writer+"\n")
                            file.close()
                            if self.help ==1:
                                self.bot.send_message(m.chat.id, "добавлено для просмотра `/update`")
                                self.help=0
                    except ZeroDivisionError:
                        self.bot.delete_message(m.chat.id, mid)
                        self.bot.send_message(m.chat.id, "Некоректный ввод цены используйте цифры")
                        self.checker=3


        @self.bot.message_handler(content_types=["photo"])
        def photo_handler(m):
            def script():
                if m.from_user.id in self.admins:
                    self.text_writer=''
                    idp = m.id
                    photo_save = self.bot.get_file(m.photo[len(m.photo) - 1].file_id)
                    download = self.bot.download_file(photo_save.file_path)
                    with open("photo.jpg", "wb") as new_file:
                        new_file.write(download)
                    text = pyzbar.decode(Image.open("photo.jpg"))
                    if text == []:
                        time.sleep(2)
                        self.bot.delete_message(m.chat.id, idp)
                        self.bot.send_message(m.chat.id, "Не вдалося розпізнати код надішліть якісне фото або вбийте код в ручну:")
                        self.checker = -1
                        time.sleep(5)
                        self.bot.delete_message(m.chat.id, idp + 1)
                    else:
                        new_text = f"{text[0].data}"[2:-1]
                        if text[0].type == "QRCODE":
                            self.bot.send_message(m.chat.id, "обнаружен QR-code:\n\n{}".format(new_text))
                        else:
                            time.sleep(1)
                            self.bot.delete_message(m.chat.id, idp)
                            self.text_writer = new_text + "@"
                            self.bot.send_message(m.chat.id, f"{new_text}\nВведiть назву товару:")
                            self.old_code ="Штрихкод: "+ new_text
                            self.new_id=idp+1
                            self.checker=1
                threading.Thread(script())


        self.bot.infinity_polling()


if __name__ == "__main__":
    try:
        Bot()
    except Exception:
        Bot().bot.close()
        Bot()
