from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class newVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Trude har på jobben hørt snakk om en ny fet todo liste webapp 
        # åpner nettleseren for å sjekke den ut
        self.browser.get('http://localhost:8000')

        # Hun legger merke til at  title og header nevner todo lister
        self.assertIn('To-Do', self.browser.title)
        header_text =     self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Hun inviteres til å skrive inn en ting som skal gjøres med det samme
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Hun skriver inn "Kjøp maggott til Bjerne" i en tekstboks
        inputbox.send_keys('Kjøp maggot')

        # Når hun trykker enter så oppdateres siden og første oppføring vises:
        # "1    Kjøp maggott til Bjerne"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Kjøp maggot', [row.text for row in rows])

        # Ennå en tekstboks inviterer til å legge til enda en oppføring. Hun 
        # skriver inn "Gi maggott til Bjerne ved neste anledning" og trykker enter.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Gi maggot til Bjerne')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Siden oppdateres igjen og begge oppføringene vises på lista.
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Kjøp maggot', [row.text for row in rows])
        self.assertIn('2: Gi maggott til Bjerne', [row.text for row in rows])

        # Trude lurer spent på om denne siden kommer til å huske hennes liste når hun lukker ned.
        # Hun er observant og legger merke til at siden har genrert en unik URL for henne --
        # det vises også noe forklarende tekst i forbindelse med lagring og den unike URL
        self.fail('Finish the test!')

        # Hun besøker denne unike URLen - hennes to-do list er der stadig vekk

        # Fornøyd vender Trude tilbake til hverdagen

        browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')