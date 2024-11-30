#include <stdio.h>
#include <math.h>

int main()
{
    long long int n = 7245415259;
    double res = sqrt(n);
    printf("%.15f\n", res);
    long long int i = 0;
    for (; i < 10000000000 ; i++)
    {
        if (sqrt(i) == res)
        {
            printf("%lld\n", i);
            break;
        }
    }
}