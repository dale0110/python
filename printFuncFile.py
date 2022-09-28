import string
import sys

def test():
    #print(f"file := {__file__}"+"line := {sys._getframe().f_lineno}"+"func :={__name__}")
    #print(f"file :=", {__file__},"line :=",{sys._getframe().f_lineno},"func :=",{__name__})
    print(__file__ ,sys._getframe().f_lineno,sys._getframe().f_code.co_name)


if __name__ == '__main__':
	test()

