from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValididtyTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Trude prøver ved en feil å sende inn en tom tekst streng. Hun trykker enter
        # i det tomme input feltet.

        # Hjemmesiden gjenlastes og det kommer en feilmelding som sier at feltet ikke kan være blankt.

        # Hun prøver igjen med noe tekst og det fungerer.

        # Perverst nok prøver hun igjen å sende inn en blank linje

        # Hun får på ny lignende feilmelding på liste siden

        # og hun kan korrigere det ved å fylle inn noe tekst
        self.fail('write me!')