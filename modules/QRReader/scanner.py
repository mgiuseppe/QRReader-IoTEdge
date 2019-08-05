from pyzbar.pyzbar import decode

class Scanner():

    def ReadQR(self, width, height, pixels):
        image = decode((pixels, width, height))

        # stampa valore
        is_detected = False
        text_value = ""
        for symbol in image:
            print ("{0}: {1}".format(symbol.type, symbol.data))
            text_value = symbol.data.decode('utf8')
            is_detected = True

        del(image)

        return (is_detected, text_value)