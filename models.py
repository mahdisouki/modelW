class Prediction:
    def __init__(self, classe, price_ex_vat, price_inc_vat):
        self._classe = classe
        self._price_ex_vat = price_ex_vat
        self._price_inc_vat = price_inc_vat

    # Getter and Setter for `classe`
    @property
    def classe(self):
        return self._classe

    @classe.setter
    def classe(self, value):
        self._classe = value

    # Getter and Setter for `price_ex_vat`
    @property
    def price_ex_vat(self):
        return self._price_ex_vat

    @price_ex_vat.setter
    def price_ex_vat(self, value):
        self._price_ex_vat = value

    # Getter and Setter for `price_inc_vat`
    @property
    def price_inc_vat(self):
        return self._price_inc_vat

    @price_inc_vat.setter
    def price_inc_vat(self, value):
        self._price_inc_vat = value

    # Convert to dictionary
    def to_dict(self):
        return {
            'classe': self.classe,
            'price_ex_vat': self.price_ex_vat,
            'price_inc_vat': self.price_inc_vat,
        }
