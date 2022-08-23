#  ==== 1 ====
class PropertyClass:
    vote_count = 10


user1 = PropertyClass()
print(user1.vote_count)
user1.vote_count = 5
print(user1.vote_count)
print(PropertyClass.vote_count)
PropertyClass.vote_count = 20
print(PropertyClass.vote_count)
user1 = PropertyClass()
print(user1.vote_count)


#  ==== 2 ====
class PropertyClass2:

    def __init__(self):
        self.vote_count = 10


print('===== 2 =====')
user1 = PropertyClass2()
print(user1.vote_count)
user1.vote_count = 5
print(user1.vote_count)
# Ishlamaydi chunki class hususiyati yo'q
# print(PropertyClass2.vote_count)
# Yangi class hususiyat yaratadi, lekin obyekt hususiyatiga tasir qilmaydi
# class hususiyatini o'zgartiradi
# PropertyClass2.vote_count = 20
# print(PropertyClass2.vote_count)
user1 = PropertyClass2()
print(user1.vote_count)


#  ==== 3 ====
class PropertyClass3:

    def __init__(self, value):
        self._vote = value

    @property
    def vote(self):
        # self.vote += 1
        return self._vote

    @vote.setter
    def vote(self, value):
        self._vote = value


print('===== 3 =====')
user1 = PropertyClass3(0)
print(user1.vote)
user1.vote = 4
print(user1.vote)


#  ==== 4 ====
# Faqat o'qish mumkin
class PropertyClass4:

    def __init__(self, value):
        self._vote = value

    @property
    def vote(self):
        return self._vote


print('===== 4 =====')
user1 = PropertyClass4(0)
print(user1.vote)
# Xatolik beradi sababi bu readonly
# user1.vote = 4
# print(user1.vote)

