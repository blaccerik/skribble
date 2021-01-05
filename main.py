from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Skribble:
    def __init__(self, file, name):
        self.words = {}
        self.read_file(file)
        self.name = name

    def read_file(self, file):
        with open(file, encoding="utf-8") as f:
            content = f.readlines()
            for i in content:
                word = i[:i.find("\n")]
                lenght = self.filter_word(word)
                self.create_dict(word, lenght)

    def filter_word(self, word):
        if " " in word:
            text = word
            a = text.split(" ")
            lenght = ""
            for i in a:
                lenght += f"{len(i)}-"
            lenght = lenght[:-1]
        else:
            lenght = str(len(word))
        return lenght

    def create_dict(self, word, lenght):
        if lenght in self.words:
            self.words[lenght].append(word.lower())
        else:
            self.words[lenght] = [word.lower()]

    def main_loop(self, auto=True):
        driver = webdriver.Firefox()
        driver.get("https://skribbl.io/")
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="cmpboxbtn cmpboxbtnyes"]').click()
        time.sleep(0.5)
        # """// input[ @ name = 'continue'][ @ type = 'button']"""
        driver.find_element_by_xpath("//input[@id='inputName']").send_keys(self.name)
        if auto:
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@class="btn btn-success btn-lg btn-block"]').click()
            time.sleep(5)
        else:
            input("Press any key")
        new_game = True
        last = None
        play = False
        while True:
            all_chat = driver.find_element_by_id("boxMessages").text
            text = all_chat
            if last != None:
                text = text[len(last) + 1:]
                # if text[0] == "\n":
                #     text = text[1:]
            last = all_chat
            # print(text.splitlines())
            time.sleep(1)
            if (f"{self.name} guessed the word!" in text and play) or "The word was" in text:
                play = False
                new_game = True
                print("Guessed")
            elif not play and new_game:
                if "is drawing now!" in text and f"{self.name} is drawing now!" not in text:
                    # play = True
                    # if new_game and play:
                    word = driver.find_element_by_id("currentWord").text
                    code = self.filter_word(word)
                    g = Game(self.words[code], word)
                    new_game = False
                    play = True


            if not new_game and play:
                word = driver.find_element_by_id("currentWord").text
                # print(word)
                g.new_word(word)
                word = g.guess()
                chat = driver.find_element_by_id("inputChat")
                chat.send_keys(word)
                chat.send_keys(Keys.RETURN)
                time.sleep(0.3)
        return

class Game:
    def __init__(self, words, word, guess=True):
        if guess:
            self.words = words
            self.word = word


    def new_word(self, word):
        if word != self.word:
            print(word)
            for i in range(len(word)):
                if word[i] == self.word[i]:
                    continue
                else:
                    self.new_letter(word[i], i)
                    self.word = word

    def new_letter(self, letter, pos):
        self.words = list(filter(lambda x: x[pos] == letter.lower(), self.words))

    def remove_word(self, word):
        if word in self.words:
            self.words.remove(word)

    def guess(self):
        if self.words == []:
            a = "tr"
            return f"{a}"
        else:
            word = self.words[0]
            self.remove_word(word)
            return word


if __name__ == "__main__":
    s = Skribble("words.txt", "Aadu")
    s.main_loop(auto=False)
    # text = "bbb\nccc\nccc"
    # text2 = "bbb\nccc\nccc\nbbb\naaa"
    # text3 = "ccc\nccc\nbbb\naaa\naaa\naaa\naaa"
    # chat = [text, text2,text3]
    # last = None
    # for i in chat:
    #     text = i
    #     if last != None:
    #         text = i[len(last) + 1:]
    #         if text[0] == "\n":
    #             text = text[1:]
    #     last = i
    #     print(text.splitlines(True))
            # break

    # test1
    # g = Game(s.words["3"], "___")
    # print(g.words)
    # g.new_word("___")
    # print(g.words)
    # g.new_word("a__")
    # print(g.words)
    # g.new_word("a__")
    # print(g.words)
    # g.new_word("ar_")
    # print(g.words)