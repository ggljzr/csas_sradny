import requests
import json
import locale
import subprocess
import curses

import pytoml as toml
import icons

config_file_path = 'config.toml'
config = {}

headers = {
	'WEB-API-KEY' : None 		
}

rows, columns = subprocess.check_output(['stty', 'size']).split()
rows = int(rows) 
columns = int(columns)

def initCurses():

	locale.setlocale(locale.LC_ALL,'')
	
	#init curses interface
	stdscr = curses.initscr()

	#colors
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

	curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLUE)

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)
	curses.curs_set(0) #no cursor
	
	return stdscr


def endCurses():
	#terminate curses application
	curses.nocbreak();curses.echo();stdscr.keypad(0)
	curses.endwin()

def draw_current_data(data, window):
	row = 1
	for entry in data:
		if entry['country'] in config['config']['countries']:
			output = entry['country'] + ' (' + entry['shortName'] + ') ' + str(entry['currBuy']) + ' ' + str(entry['currSell'])
			window.addstr(row, 0, output)
			row = row + 1
	window.refresh();

def draw_countries_menu(menu_window):
	row = 0
	for country in config['config']['countries']:
		menu_window.addstr(row, 0, country)
		row = row + 1
	menu_window.refresh()

def draw_country_data(data_window, data, country):
	country_data = data[0]
	for entry in data:
		if entry['country'] == country:
			country_data = entry
	
	data_window.clear()

	max_width = len('Současný prodej: ' + str(country_data['currSell']))

	data_window.addstr(0,0, 'Země: ' + country)
	data_window.addstr(1,0, country_data['name'] + ' (' +country_data['shortName'] + ')')
	data_window.addstr(2,0, 'Platnost: ' + country_data['validFrom'])
	data_window.addstr(3,0, 'Množství: ' + str(country_data['amount']))
	data_window.addstr(4,0, 'Současný výkup: ' + str(country_data['currBuy']))
	data_window.addstr(5,0, 'Současný střed: ' + str(country_data['currMid']))
	data_window.addstr(6,0, 'Současný prodej: ' + str(country_data['currSell']))
	data_window.addstr(7,0, 'Změna: ' + str(country_data['move']))
	data_window.addstr(8,0, 'Kurz ČNB: ' + str(country_data['cnbMid']))
	
	icon = icons.none;
	if country_data['move'] > 0:
		icon = icons.up
	elif country_data['move'] < 0:
		icon = icons.down

	icons.drawIcon(max_width + 1, 1, icon, data_window);

	data_window.refresh();

def draw_menu_select(menu_window, item, direction):
	menu_items = len(config['config']['countries'])
	item_next = (item + direction * -1) % menu_items
	menu_window.addstr(item, 0, config['config']['countries'][item], curses.color_pair(8) | curses.A_BOLD)
	menu_window.addstr(item_next,0, config['config']['countries'][item_next])
	menu_window.refresh()


if __name__ == '__main__':
	with open(config_file_path) as config_file:
		config = toml.load(config_file)
	
	headers['WEB-API-KEY'] = config['api']['key']
	
	request = requests.get('https://api.csas.cz/sandbox/webapi/api/v1/exchangerates', headers = headers)
	
	if request.status_code != 200:
		exit()

	json_data = request.json()
	
	stdscr = initCurses()
	stdscr.refresh()

	max_width = 0
	for country in config['config']['countries']:
		if len(country) > max_width:
			max_width = len(country)
	
	#menu pro vyber zeme, uplne v pravo
	current_item = 0
	menu_items = len(config['config']['countries'])
	menu_window = curses.newwin(rows, max_width, 0, 0)
	draw_countries_menu(menu_window)
	draw_menu_select(menu_window, 0, 1)

	#okno pro zobrazeni dat zvolene zeme
	data_window = curses.newwin(rows, columns - (max_width + 1), 0, max_width + 1)
	draw_country_data(data_window, json_data, config['config']['countries'][0])

	while True:
		c = stdscr.getch()
		if c == ord('q'):
			break
		if c == curses.KEY_UP:
			current_item = (current_item - 1) % menu_items
			draw_menu_select(menu_window, current_item, -1)
			draw_country_data(data_window, json_data, config['config']['countries'][current_item])
		if c == curses.KEY_DOWN:
			current_item = (current_item + 1) % menu_items
			draw_menu_select(menu_window, current_item, 1)
			draw_country_data(data_window, json_data, config['config']['countries'][current_item])

	endCurses()

