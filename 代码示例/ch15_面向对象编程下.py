# -*- coding: utf-8 -*-
"""
第 15 章：面向对象编程（下）
对应教材：第二部分-Python进阶/15-面向对象编程下.md

演示：继承、super()、方法重写、多态、私有属性、@property、
      @classmethod 与 @staticmethod。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 继承：复用父类的代码")


class Animal:                # 父类（基类）
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} 在吃东西")


class Dog(Animal):           # 子类，括号里写父类名
    def bark(self):
        print(f"{self.name} 汪汪叫")


class Cat(Animal):
    def meow(self):
        print(f"{self.name} 喵喵叫")


d = Dog("旺财")
d.eat()      # 旺财 在吃东西（继承自 Animal）
d.bark()     # 旺财 汪汪叫（Dog 自己的）

section("2. super()：调用父类方法")


class Dog2(Animal):
    def __init__(self, name, breed):
        super().__init__(name)    # 调用父类的 __init__，设置 name
        self.breed = breed         # 再补充自己的属性


d2 = Dog2("旺财", "金毛")
print(d2.name, d2.breed)          # 旺财 金毛

section("3. 方法重写（Override）")


class Animal2:
    def speak(self):
        print("动物发出声音")


class Dog3(Animal2):
    def speak(self):                 # 重写父类的 speak
        print("汪汪汪")


class Cat2(Animal2):
    def speak(self):
        print("喵喵喵")


Animal2().speak()    # 动物发出声音
Dog3().speak()       # 汪汪汪（用子类自己的版本）
Cat2().speak()       # 喵喵喵

section("4. 多态：同样的调用，不同的表现")

# 注意：这里沿用 15.3 的简化版 Animal2/Dog3/Cat2（无参构造）
animals = [Dog3(), Cat2(), Animal2()]
for animal in animals:
    animal.speak()      # 每个对象调用自己的 speak

# 鸭子类型：不关心具体类型，只要有 speak() 方法就行
d = Dog3()
print(isinstance(d, Dog3))       # True
print(isinstance(d, Animal2))    # True（Dog3 也是 Animal2）

section("5. 封装与私有属性")


class BankAccount:
    def __init__(self, balance):
        self.__balance = balance      # 双下划线：名称改写，外部难直接访问

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance


acc = BankAccount(100)
acc.deposit(50)
print(acc.get_balance())     # 150
# print(acc.__balance)       # 故意错误示范：外部访问不到（已省略）

section("6. @property：把方法用成属性")


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):                  # 像属性一样，不用 ()
        return 3.14159 * self.radius ** 2


c = Circle(5)
print(c.area)        # 78.53975（注意没有括号！）


class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):        # 赋值时做校验
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value


t = Temperature()
t.celsius = 25           # 触发 setter（含校验）
print(t.celsius)         # 25

section("7. 类方法与静态方法")


class Pizza:
    count = 0

    def __init__(self, size):
        self.size = size
        Pizza.count += 1

    @classmethod
    def total_made(cls):             # 类方法，操作类本身（cls）
        return cls.count

    @staticmethod
    def is_valid_size(size):         # 静态方法：逻辑上属于类的工具函数
        return size in ("小", "中", "大")


Pizza("大")
Pizza("中")
print(Pizza.total_made())            # 2
print(Pizza.is_valid_size("超大"))   # False

# md 练习题第 1 题：继承 + 多态
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class Circle2(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

for s in [Square(4), Circle2(3), Square(2)]:
    print(f"{type(s).__name__} 面积：{s.area():.2f}")

# md 练习题第 2 题：员工与经理
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    def info(self):
        return f"{self.name}，薪资 {self.salary}"

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus
    def info(self):
        base = super().info()
        return f"{base}，奖金 {self.bonus}，总计 {self.salary + self.bonus}"

print(Manager("小明", 10000, 5000).info())

print("\n第 15 章演示完毕 ✅")
