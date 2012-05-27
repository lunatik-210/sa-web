#include <iostream>

int func1();

int func2();

int func3();

int func4();

int main()
{
	return func1();
}

int func1()
{
	return func2();
}

int func2()
{
	return func3();
}

int func3()
{
	return 0;
}

int func4()
{
	return func3();
}