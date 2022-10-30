from zope import interface

class warInterface(interface.Interface):
    
    
    name = interface.Attribute(
        "user name"
    )
    
    computerCards = interface.Attribute(
        "computer's cards"
    )
    
    userCards = interface.Attribute(
        "user's cards"
    )
    
    def getNextUserCard():
        "What is the user's next card?"
        
    def getNextComputerCard():
        "What is the computer's next card?"
        
    def removeNextUserCard():
        "Remove the top card from the user's deck"
    
    def removeNextComputerCard():
        "Remove the top card from the computer's deck"
    
    