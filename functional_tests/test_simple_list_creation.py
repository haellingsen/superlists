from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):    

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Trude har på jobben hørt snakk om en ny fet todo liste webapp 
        # åpner nettleseren for å sjekke den ut
        self.browser.get(self.live_server_url)

        # Hun legger merke til at  title og header nevner todo lister
        self.assertIn('To-Do', self.browser.title)
        header_text =     self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Hun inviteres til å skrive inn en ting som skal gjøres med det samme
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Hun skriver inn "Kjøp maggott til Bjerne" i en tekstboks
        inputbox.send_keys('Kjøp maggot')

        # Når hun trykker enter så oppdateres siden og første oppføring vises:
        # "1    Kjøp maggott til Bjerne"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp maggot')

        # Ennå en tekstboks inviterer til å legge til enda en oppføring. Hun 
        # skriver inn "Gi maggott til Bjerne" og trykker enter.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Gi maggot til Bjerne')
        inputbox.send_keys(Keys.ENTER)

        # Siden oppdateres igjen og begge oppføringene vises på lista.
        self.wait_for_row_in_list_table('1: Kjøp maggot')
        self.wait_for_row_in_list_table('2: Gi maggot til Bjerne')

        # Trude lurer spent på om denne siden kommer til å huske hennes liste når hun lukker ned.
        # Hun er observant og legger merke til at siden har genrert en unik URL for henne --
        # det vises også noe forklarende tekst i forbindelse med lagring og den unike URL

        # Hun besøker denne unike URLen - hennes to-do list er der stadig vekk

        # Fornøyd vender Trude tilbake til søvnen
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # True starter en ny liste
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Kjøp maggot')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp maggot')

        # Hun legger merke til at hennes liste har en unik URL
        trude_list_url = self.browser.current_url
        self.assertRegex(trude_list_url, '/lists/.+')

        # Det kommer en ny bruker til siden.

        ## Vi benytter en ny browser session for å være sikker på at ingen informasjon
        ## fra Trudes kommer gjennom cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Frans besøker siden. Det er ingen tegn til Trudes liste.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kjøp maggot', page_text)
        self.assertNotIn('make a fly', page_text)

        # Frans starter en ny liste ved å legge inn en ny oppføring. Han
        # er mindre interessant enn Trude
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Kjøp melk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Kjøp melk')

        # Frans får sin egen unike URL
        frans_list_url = self.browser.current_url
        self.assertRegex(frans_list_url, '/lists/.+')
        self.assertNotEqual(frans_list_url, trude_list_url)

        #Til slutt det er ingen spor av Trudes liste
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Gi maggot til Bjerne', page_text)
        self.assertIn('Kjøp melk', page_text)

        # Begge fornøyde vender tilbake til søvnriket