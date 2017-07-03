from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidityTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Trude prøver ved en feil å sende inn en tom tekst streng. Hun trykker enter
        # i det tomme input feltet.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Browseren blander seg opp i requesten og laster ikke listesiden
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # Hun prøver igjen, skriver noe tekst i feltet og feilen forsvinner
        self.get_item_input_box().send_keys('Kjøp melk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        # Hun kan nå sende forespørselen
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp melk')

        # Perverst nok prøver hun igjen å sende inn en blank linje
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Nok en gang vil ikke browseren ha noe med dette å gjøre og viser feilmeldingen
        self.wait_for_row_in_list_table('1: Kjøp melk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # og hun kan korrigere det ved å fylle inn noe tekst
        self.get_item_input_box().send_keys('Lag te')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp melk')
        self.wait_for_row_in_list_table('2: Lag te')

    def test_cannot_add_duplicate_items(self):
        # Trude åpner hjemmesida og starter ei ny liste
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Kjøp fisk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp fisk')

        # Tilfeldigvis prøver hun å legge inn samme tekst igjen
        self.get_item_input_box().send_keys('Kjøp fisk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # Hun ser en hjelpsom feilmelding
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text, 
            "You've already got this one in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Trudis starter en liste og forårsaker en valideringsfeil:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # Hun starter og skrive i input box for å klarere feilen
        self.get_item_input_box().send_keys('a')

        # Hun er fornøyd med å se at feilmeldingen forsvinner
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
