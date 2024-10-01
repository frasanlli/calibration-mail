from log import Log

class Main_class(Log):
    #def __init__(self) -> None:


    def main(self) -> None:
        pass
        #Create frame
        #Frame checks necessary updates on DB products on start (run check method)
        #If a match is found, it asks if you want to send a mail about it
        #It continues until all matches are asked
        #Then, you can:
            #add new products to DB
                #If you add a product, it is necessary a picture of the calibration date and a pdf with the instructions
            #You can modify products attributes
                #If you modify a product's calibration you need to update the current picture of the tag
                #If you add a new product's calibration you need to add a new picture.
                    #The creation date of the picture will be checked, to be sure it is not the same as an old one
            #Check products, same function as initial
        #A red text will appear with the DB products out of date
        #An orange text will appear with the DB products near to expiration date:
            #Set days before the expiration date you want to be advised
        #A green text will appear if all the DB products are fine
        #A blue text will show products that are in process of being adjusted
            #If a product cannot be adjusted then it will require a pdf or mail that probes that

if __name__ == '__main__':
    main_process = Main_class()
    main_process.main()