from random import choice, randint
import math
from string import digits
import threading

class Parasitic_Number(object):
    """A Parasitic number (in base 10) is a Positive natural number which can be multiplied by n by moving the rightmost digit of its decimal representation to the front.
        102564 × 4 = 410256
        142857 × 5 = 714285
        179487 × 4 = 717948
        105263157894736842 × 2 = 210526315789473684
        1014492753623188405797 × 7 = 7101449275362318840579  """

    def __init__(self) -> None:
        self.parasitic_numbers = {}
        self.count = 0
        self.thread_list = []

    def import_parasitic_nums(self, file:str) -> None:
        with open(file, 'r', encoding='utf-8') as f:
            for num in f.readlines():
                num = num.replace('\n', '')
                if self.check_parasitic_property(num):
                    self.parasitic_numbers[num] = True
                    self.count+=1
                else:
                    print('False', num)
    
    def export_new_numbers(self, file:str) -> None:
        with open(file, 'w', encoding='utf-8') as f:
            for key in self.parasitic_numbers:
                f.write(key+'\n')

    def first_n_digits(self, num:int, n:int) -> int:
        return num // 10 ** (int(math.log(num, 10)) - n + 1)

    def last_digit(self, num:int ) -> int:
        return num % 10

    def check_parasitic_property(self, num:str ) -> bool:
        if num == len(num) * num[0]:
            return False
        new_number = int(num[1:] + num[0])
        num = int(num)
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if new_number * n == num:
                return True
        return False

    def random_parasitic_numbers(self, min:int, max:int, amount=1) -> None:
        amount+=self.count
        while(len(self.parasitic_numbers) < amount):
            length = randint(min, max)
            number = ''.join(choice(digits) for i in range(length))
            if self.check_parasitic_property(number) and number not in self.parasitic_numbers:
                self.parasitic_numbers[number] = True
                print(number)

    def exhaustive_parasitic_numbers(self, start, end) -> None:
        for number in range(start, end):
            number = str(number)
            if self.check_parasitic_property(number) and number not in self.parasitic_numbers:
                self.parasitic_numbers[number] = True
                print(number)

    def brute_force(self, num_threads:int, min:int, max:int, method='exhaustive', amount=1) -> None:
        if method=='randomized':
            for i in range(num_threads):
                x = threading.Thread(target=self.random_parasitic_numbers, args=(min, max, amount))

        elif method == 'exhaustive':
            start, end = 1, 1
            for i in range(min-1):
                start = start * 10
            for i in range(max-1):
                end = end * 10
            work_per_thread = (end - start) // num_threads
            print('Work per Thread:', work_per_thread)
            end_of_work = start + work_per_thread
            for i in range(num_threads):
                if i == 0:
                    print('Thread:', i, 'start of work:', start, 'end of work', end_of_work )
                    x = threading.Thread(target=self.exhaustive_parasitic_numbers, args=(start, end_of_work) )
                else:
                    start_of_work = end_of_work
                    end_of_work+=work_per_thread
                    print('Thread:', i, 'start of work:', start_of_work, 'end of work', end_of_work)
                    if i==num_threads:
                        end_of_work=end
                    x = threading.Thread(target=self.exhaustive_parasitic_numbers, args=(start_of_work, end_of_work) )

                self.thread_list.append(x)
                x.start()

            for thread in self.thread_list:
                thread.join()

if __name__ == '__main__':
    para = Parasitic_Number()
    para.import_parasitic_nums('known_parasitic_numbers.txt')
    para.brute_force(num_threads=8, min=2, max=16, method='exhaustive')
    para.export_new_numbers('known_parasitic_numbers.txt')