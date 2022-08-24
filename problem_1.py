import random, string
class Password:
    #input password
    def input_password(self):
        print("Write your words:")
        try:
            self.__password = str(input())
            if len(self.__password) >= 8:
                return p.mix_characters(self.__password)
            else:
                self._new_char = 8 - len(self.__password)
                self._out_generate = ""
                for _ in range(self._new_char):
                    self._random = random.choice(string.ascii_letters)
                    self._out_generate = self._out_generate + self._random
                self._password_add = self.__password + self._out_generate
                return p.mix_characters(self._password_add)
        except:
            print("Error input.")

    def mix_characters(self, password):
        self.__password = str(password)
        self._mix_password = ''.join(random.sample(self.__password,len(self.__password)))
        return self._mix_password
p = Password()
print("Generated password --> \"{0}\" ".format(p.input_password()))
