# from site_parser import Parser
from site_parser import InstagramParser
import time

# parser = Parser(driver_type='chrome')
parser = InstagramParser(username='aawra.ee', password='Rgfd4532bnH')

driver = 0
refs = []
max_likes = 100
max_follows = 150

parser.start_parse()
