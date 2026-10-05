# -*- coding: utf-8 -*-
"""
第 14 章：面向对象编程（上）
对应教材：第二部分-Python进阶/14-面向对象编程上.md

演示：类与对象、__init__ 与 self、属性与方法（银行账户）、
      实例属性 vs 类属性、__str__。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 定义第一个类")


class Dog:
    def bark(self):
        print("汪汪汪！")


my_dog = Dog()        # 创建对象（实例化），注意有括号
my_dog.bark()         # 汪汪汪！

section("2. __init__ 与 self")


class Dog:
    def __init__(self, name, age):
        self.name = name      # 把参数保存为对象的属性
        self.age = age

    def bark(self):
        print(f"{self.name} 说：汪汪汪！")
    # self 代表对象自己：调用 dog1.bark() 时，Python 自动把 dog1 传给 self


dog1 = Dog("旺财", 3)    # 创建时传入的参数会自动传给 __init__
dog2 = Dog("小黑", 5)

print(dog1.name)     # 旺财，访问属性
print(dog2.age)      # 5
dog1.bark()          # 旺财 说：汪汪汪！
dog2.bark()          # 小黑 说：汪汪汪！

section("3. 属性与方法：银行账户")


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"存入 {amount}，余额 {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("余额不足！")
        else:
            self.balance -= amount
            print(f"取出 {amount}，余额 {self.balance}")


acc = BankAccount("小明", 100)
acc.deposit(50)       # 存入 50，余额 150
acc.withdraw(200)     # 余额不足！
acc.withdraw(80)      # 取出 80，余额 70

section("4. 实例属性 vs 类属性")


class Dog2:
    species = "犬科"          # 类属性：所有对象共享

    def __init__(self, name):
        self.name = name       # 实例属性：每个对象各有一份


d1, d2 = Dog2("旺财"), Dog2("小黑")
print(d1.species, d2.species)  # 犬科 犬科（共享同一个）
print(Dog2.species)            # 也能通过类名访问
print(d1.name, d2.name)        # 旺财 小黑（各自不同）


# 类属性统计：一共创建了多少个对象
class Counter2:
    count = 0

    def __init__(self, name):
        self.name = name
        Counter2.count += 1

Counter2("A")
Counter2("B")
Counter2("C")
print("共创建：", Counter2.count)   # 3

section("5. __str__：让对象更可读")


class Dog3:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"狗狗({self.name}, {self.age}岁)"   # 自定义打印时的显示内容


d = Dog3("旺财", 3)
print(d)              # 狗狗(旺财, 3岁)（而不是看不懂的内存地址）

# md 练习题第 1 题：学生类
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_pass(self):
        return self.score >= 60

print(Student("小明", 55).is_pass())    # False
print(Student("小红", 88).is_pass())    # True

# md 练习题第 2 题：矩形类
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(3, 4)
print(r.area(), r.perimeter())          # 12 14

# md 练习题第 3 题：计数器类
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def __str__(self):
        return f"当前计数：{self.count}"

c = Counter()
c.increment()
c.increment()
print(c)              # 当前计数：2
c.reset()
print(c)              # 当前计数：0

print("\n第 14 章演示完毕 ✅")
