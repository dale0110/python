import time
import datetime

#计时器装饰器
def timer(func):
    def func_wrapper(*args,**kwargs):
        start_time = time.time()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        result=func(*args,**kwargs)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        end_time = time.time()
        time_spend = (end_time - start_time)
        print('\n{0} cost time {1} s\n'.format(func.__name__, time_spend))
        return result
    return func_wrapper



#测试结果
#请输入一个整数：1000000
#2023-03-06 14:06:52.364
#78496
#2023-03-06 14:06:56.708

#counter_primer cost time 4.343954801559448 s

#判断是否为素数（质数）
#质数还有一个特点，除了 2 和 3，它总是等于 6x-1 或者 6x+1，其中 x 是大于等于1的自然数
def isPrime(a):

    if a==2 or a==3:
        return True

    #质数还有一个特点，除了 2 和 3，它总是等于 6x-1 或者 6x+1，其中 x 是大于等于1的自然数
    if a%6!=1 and a%6!=5:
        return False

    for i in range(2, int(a**0.5)+1,1):
        if a%i==0:
            return False

    return True


#slow测试结果：
#请输入一个整数：1000000
#2023-03-06 14:07:47.004
#78498
#2023-03-06 14:08:30.834

#counter_primer cost time 43.83078670501709 s
def isPrime_slow(a):
    rc=True
    for i in range(2, int(a**0.5)+1):
        if a%i==0:
            rc=False
    return rc


#求取最大公约数:欧几里得算法
def gcd(a, b):
    #如果b大于a，则将a、b交换
    if b>a :
        a,b=b,a

    # 辗转相除法取最大公约数
    while b != 0:
        a, b = b, a % b
    return a


#求最小公倍数（Lowest Common Multiple）
#原理是两个数的最小公倍数会等于两个数的乘积除以两个数的最大公约数的结果。即：
#LCM(a, b) = (a * b) / GCD(a, b）

def lcm(a, b):
    return (a * b) / gcd(a, b)

@timer
def counter_primer(num):
    counter=0
    for i in range(2, num):
        if isPrime(i):
            counter+=1
            #print(i)

    print(counter)
    return counter


#测试结果
#请输入一个整数：1000000
#2023-03-06 15:15:21.348
#78498
#2023-03-06 15:15:26.137
#print_primer cost time 4.788947343826294 s
'''
请输入一个整数：100000000
2023-03-06 15:23:18.821
5761453
2023-03-06 16:03:17.651

print_primer cost time 2398.8306472301483 s
'''
@timer
def print_primer(num):
    ListPrimer = [2,3]
    counter=0

    for i in range(4, num):
        isPrime=False
        if i % 6 != 1 and i % 6 != 5:
            isPrime = False
            continue

        for j in range(0, len(ListPrimer) , 1):
            if ListPrimer[j]>int(i**0.5):
                isPrime = True
                break
            if i % ListPrimer[j] == 0:
                isPrime = False
                break

        if isPrime:
            #print(i)
            ListPrimer.append(i)
            counter +=1

    print(counter)



'''
num1 =int(input("请输入一个整数："))

num2 =int(input("请输入一个整数："))

rc_gcd=gcd(num1,num2)
rc_lcm=lcm(num1,num2)

print(rc_gcd,rc_lcm)
'''

num1 =int(input("请输入一个整数："))

#counter_primer(num1)
print_primer(num1)
