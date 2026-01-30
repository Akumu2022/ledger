from decimal import Decimal


class Reconciliation:
    def __init__(self):
        self.mismatches = []

    def compare(self, internal_amount: Decimal, external_amount: Decimal):
        if internal_amount != external_amount:
            diff = external_amount - internal_amount
            self.mismatches.append(diff)
            return False
        return True
