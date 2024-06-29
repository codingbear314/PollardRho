#PollardRho.py
#By js314 (Jaewook Jung)
import random
def FastFactorize(N:int, sort:bool=True, seed:int=-1)->list[int]:
    #Simple GCD function
    def GCD(a, b):
        while b!=0:
            a, b=b, a%b
        return a

    #Fast powering using divide and conquer
    def Power(x, y, mod):
        x%=mod
        answer=1
        while y>0:
            if y%2==1:
                answer=(answer*x)%mod
            y//=2
            x=(x**2)%mod
        return answer
    
    #MillerRabin prime test
    def MillerRabin(n, a):
        # first of all, n is odd
        k=0
        m=n-1
        while m%2==0:
            k+=1
            m//=2
        # Since we know n is odd, we can rewrite n-1 as 2^k*m
            
        b0=Power(a, m, n)

        # if b0 is 1 or n-1, then n is probably prime, due to Fermat's little theorem (reversed)
        # This is "probably prime", not "prime". So, miller-rabin test is not 100% accurate.
        if b0==1 or b0==n-1:
            return True
        else:
            for _ in range(k-1):
                b0=(b0**2)%n
                if b0==n-1:
                    return True
        return False
    
    #Wrapper for miller-rabin test
    def IsPrime(n):
        if n==1:
            return False
        if n in (2,3):
            return True
        if not n%2:
            return False
        for k in (2,3,5,7,11,13,17,19,23,29,31,37,41):
            if n==k:
                return True
            if not MillerRabin(n, k):
                return False
        return True
    
    PollardRhoWaitStack=[]

    #Iterative function, doing pollard rho
    #Note that this algorithm only finds a prime factor, not factorize it
    #So, we need a wrapper for it
    def PollardRhoIterative(n):
        # The main idea of Pollard Rho is that,
        # In a function f(x)=(x^2+c)%p, where p is a factor of n,
        # x, f(x), f(f(x)), ... is a cycle, and if a,b is in the cycle, and
        # if a, b has the same remainder when divided by p, then
        # a, b is in a cycle.
        # So, a-b is divisible by p, and n is divisible by p.
        # So, we can find a factor of n by GCD(a-b, n).
        if n==1:
            return 1
        if n%2==0:
            return 2
        if IsPrime(n):
            return n

        x=random.randint(2,n)
        y=x
        z=random.randint(1,n)
        possible_factor=1


        # if possible_factor==1, then we need to try again
        while possible_factor==1:
            x=((x**2)%n+z)%n
            y=((y**2)%n+z)%n
            y=((y**2)%n+z)%n
            possible_factor=GCD(abs(x-y), n)

            # The random is not good enough
            if possible_factor==n:
                PollardRhoWaitStack.append(n)
                return None
        if IsPrime(possible_factor):
            return possible_factor
        else:
            PollardRhoWaitStack.append(possible_factor)
            return None

    #A wrapper for PollardRhoRecursive
    #This really factorizes the number
    def PollardRho(n, sort, seed):
        if seed!=-1:
            random.seed(seed)

        factors=[]
        while n>1:
            PollardRhoWaitStack.append(n)
            while PollardRhoWaitStack:
                now=PollardRhoWaitStack.pop()
                factor=PollardRhoIterative(now)
                if factor!=None:
                    factors.append(factor)
                    n//=factor


        if sort:
            factors.sort()
        return factors

    return PollardRho(N, sort, seed)


if __name__=="__main__":
    #Example
    print(FastFactorize(1000000000100000000002379))