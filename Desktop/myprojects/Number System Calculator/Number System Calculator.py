
      
convert = int(input('''Enter
    1 for Decimal to Binary
    2 for Binary to Decimal
    3 for Decimal to Hexadecimal
    4 for Hexadecimal to Binary
    5 for Binary to Hexadecimal
    6 for Hexadecimal to Binary: '''))

def DecimalToBinary():
    number = int(input("Enter a decimal number: "))
    remainder = ''
    while number != 0:
        number = number // 2
        remainder = str(number % 2) + remainder
    return remainder





if convert == 1:
    print(DecimalToBinary())    
else:
    print("Invalid output")



