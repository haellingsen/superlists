from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValididtyTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Trude prøver ved en feil å sende inn en tom tekst streng. Hun trykker enter
        # i det tomme input feltet.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Hjemmesiden gjeninnlastes og det kommer en feilmelding som sier at feltet ikke kan være blankt.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # Hun prøver igjen med noe tekst og det fungerer.
        self.get_item_input_box().send_keys('Kjøp melk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp melk')

        # Perverst nok prøver hun igjen å sende inn en blank linje
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Hun får på ny lignende feilmelding på liste siden
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # og hun kan korrigere det ved å fylle inn noe tekst
        self.get_item_input_box().send_keys('Lag te')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp melk')
        self.wait_for_row_in_list_table('2: Lag te')