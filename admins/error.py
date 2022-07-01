class OfferAmountError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, offer, message="offer greater than product price"):
        self.offer = offer
        self.message = message
        super().__init__(self.message)