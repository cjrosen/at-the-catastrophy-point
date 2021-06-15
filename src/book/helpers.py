
class Helpers(object):

    @classmethod
    def to_roman(self, i):
        intToroman = { 1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
              50: 'L', 90: 'XC', 100: 'C', 400: 'XD', 500: 'D', 900: 'CM', 1000: 'M'}
        
        #Descending intger equivalent of seven roman numerals 
        print_order = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

        roman = ""
        for x in print_order:
            if i != 0:
                quotient= i//x

                #If quotient is not zero output the roman equivalent
                if quotient != 0:
                    for y in range(quotient):
                        roman += intToroman[x]

                #update integer with remainder
                i = i%x
        return roman.lower()

if __name__ == '__main__':
    print([Helpers.to_roman(i) for i in range(1,26)])