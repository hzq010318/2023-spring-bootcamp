def wrapping_paper(func):
    def wrapped(gift: int):
        return 'I got a wrapped up {} for you'.format(str(func(gift)))

    return wrapped


@wrapping_paper
def gift_func(giftname: int) -> str:
    return giftname


print(gift_func('gtx 5000'))
print(wrapping_paper.__annotations__)
print(gift_func.__annotations__)

# https://www.geeksforgeeks.org/function-decorators-in-python-set-1-introduction/