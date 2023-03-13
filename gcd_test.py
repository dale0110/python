import time
import datetime

import code, traceback, signal

def debug(sig, frame):
    """
    Interrupt running process, and provide a python prompt for
    interactive debugging.
    """
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  ="Signal received : entering python shell.Traceback:"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler

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

@timer
def print_primer(num):
    ListPrimer = [2,3]
    counter=0

    for i in range(4, num):
        isPrime=False
        if i % 6 != 1 and i % 6 != 5:
            isPrime = False
            continue

        #迭代相除已知质数进行测试
        for j in range(0, len(ListPrimer) , 1):
            # 如果操作超过平方根则测试结束
            if ListPrimer[j]>int(i**0.5):
                isPrime = True
                break
            # 如果能够被整除，则结束
            if i % ListPrimer[j] == 0:
                isPrime = False
                break
        # 如果当前i为质数，则登记到已知质数列表
        if isPrime:
            #print(i)
            ListPrimer.append(i)
            counter +=1

    print(counter)

#给出小于num的素数列表，num要大于4
def find_Primer_list(num):
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

    return ListPrimer


''''
请输入一个整数：23698763
2023-03-07 13:54:51.617
11 : 1 方
23 : 1 方
47 : 1 方
1993 : 1 方
778773
2023-03-07 13:57:03.362

div_composite_num cost time 131.74415349960327 s

请输入一个整数：123874676
2023-03-07 14:23:13.253
2 : 2 方
827 : 1 方                                                                                                                                                                                    
37447 : 1 方                                                                                                                                                                                  
3670110                                                                                                                                                                                       
2023-03-07 14:44:25.411                                                                                                                                                                       
                                                                                                                                                                                              
div_composite_num cost time 1272.158326625824 s 
'''
#对于num进行合数分解，result_dict返回的质数词典
@timer
def div_composite_num(num):
    primer_list=find_Primer_list(int(num/2))

    result_dict={}

    #primer_dict={}
    #列表转换为词典
    #primer_dict=dict(zip(primer_list, [0]*len(primer_list)))

    i=0
    while True:
        if  num<2:
            break

        if i>=len(primer_list):
            break
        #判断当前质数能否被整除，如果能被整除，则继续尝试能否被整除
        if num%primer_list[i]==0:
            #该质数分解次数增加+1
            if primer_list[i] in result_dict:
                result_dict[primer_list[i]] += 1
            else:
                result_dict[primer_list[i]] = 1
            #准备下一次整除重置num值
            num /= primer_list[i]
        #不能整除，则尝试下一个质数
        else:
            i+=1

    for primer  in result_dict:
        print(primer, ":", result_dict[primer], "方")

    return  result_dict



'''
num1 =int(input("请输入一个整数："))

num2 =int(input("请输入一个整数："))

rc_gcd=gcd(num1,num2)
rc_lcm=lcm(num1,num2)

print(rc_gcd,rc_lcm)
'''
listen()
num1 =int(input("请输入一个整数："))

#counter_primer(num1)
#print_primer(num1)

div_composite_num(num1)
