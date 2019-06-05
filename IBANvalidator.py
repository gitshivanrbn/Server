import websockets
import asyncio
import json


IBAN = 'SU00PAVL963150'
decodedIBAN = ""


class IBANvalidator:
    def __init__(self):
        self = self

    def validateIBAN(self,IBAN):
        controlnumber = int(IBAN[2:4])
        print('control number is ',controlnumber)
        if (controlnumber < -99 or controlnumber > 98):
            print('control number invalid')
            return False
        else:
            IBAN = IBAN[4:14]+IBAN[0:4]
            print('moved IBAN is ',IBAN)
            decodedIBAN = ''
            print(IBAN[0:4])
            for c in IBAN:
                if (c == 'a' or c == 'A'):
                    decodedIBAN += str('10') 
                    print('String contained A')
                elif (c == 'b' or c == 'B'):
                    decodedIBAN += str('11')
                    print('String contained B')
                elif (c == 'c' or c == 'C'):
                    decodedIBAN += str('12')
                    print('String contained C')
                elif (c == 'd' or c == 'D'):
                    decodedIBAN += str('13')
                    print('String contained D')
                elif (c == 'e' or c == 'E'):
                    decodedIBAN += str('14')
                    print('String contained E')
                elif (c == 'f' or c == 'F'):
                    decodedIBAN += str('15')
                    print('String contained F')
                elif (c == 'g' or c == 'G'):
                    decodedIBAN += str('16')
                    print('String contained G')
                elif (c == 'h' or c == 'H'):
                    decodedIBAN += str('17')
                    print('String contained H')
                elif (c == 'i' or c == 'I'):
                    decodedIBAN += str('18')
                    print('String contained I')
                elif (c == 'j' or c == 'J'):
                    decodedIBAN += str('19')
                    print('String contained J')
                elif (c == 'k' or c == 'K'):
                    decodedIBAN += str('20')
                    print('String contained K')
                elif (c == 'l' or c == 'L'):
                    decodedIBAN += str('21')
                    print('String contained L')
                elif (c == 'm' or c == 'M'):
                    decodedIBAN += str('22')
                    print('String contained M')
                elif (c == 'n' or c == 'N'):
                    decodedIBAN += str('23')
                    print('String contained N')
                elif (c == 'o' or c == 'O'):
                    decodedIBAN += str('24')
                    print('String contained O')
                elif (c == 'p' or c == 'P'):
                    decodedIBAN += str('25')
                    print('String contained P')
                elif (c == 'q' or c == 'Q'):
                    decodedIBAN += str('26')
                    print('String contained Q')
                elif (c == 'r' or c == 'R'):
                    decodedIBAN += str('27')
                    print('String contained R')
                elif (c == 's' or c == 'S'):
                    decodedIBAN += str('28')
                    print('String contained S') 
                elif (c == 't' or c == 'T'):
                    decodedIBAN += str('29')
                    print('String contained T')
                elif (c == 'u' or c == 'U'):
                    decodedIBAN += str('30')
                    print('String contained U')
                elif (c == 'v' or c == 'V'):
                    decodedIBAN += str('31')
                    print('String contained V')
                elif (c == 'w' or c == 'W'):
                    decodedIBAN += str('32')
                    print('String contained W')
                elif (c == 'x' or c == 'X'):
                    decodedIBAN += str('33')
                    print('String contained X')
                elif (c == 'y' or c == 'Y'):
                    decodedIBAN += str('34')
                    print('String contained Y')
                elif (c == 'm' or c == 'Z'):
                    decodedIBAN += str('35')
                    print('String contained Z')
                elif ( c == ' '):
                    print('space here')




                else:
                    decodedIBAN += str(c)
            print('decoded IBAN = ',decodedIBAN)
            validatedIBAN = int(decodedIBAN) % 97
            #validatedIBAN = 98 - validatedIBAN
            print(validatedIBAN)
            return True


a = IBANvalidator()
check = a.validateIBAN(IBAN)
print(check)
