#code:
#1 = black
#2 = green
#3 = red
#1 = grey

import curses

iconWidth = 8
iconHeight = 8

up = [
	[1,1,1,2,2,2,2,2],
	[1,1,1,1,1,2,2,2],
	[1,1,1,1,2,2,2,2],
	[1,1,1,2,2,2,1,2],
	[1,1,2,2,2,1,1,2],
	[1,2,2,2,1,1,1,1],
	[2,2,2,1,1,1,1,1],
	[2,2,1,1,1,1,1,1]]

down = [
	[1,1,1,1,1,1,3,3],
	[1,1,1,1,1,3,3,3],
	[1,1,1,1,3,3,3,1],
	[3,1,1,3,3,3,1,1],
	[3,1,3,3,3,1,1,1],
	[3,3,3,3,1,1,1,1],
	[3,3,3,1,1,1,1,1],
	[3,3,3,3,3,1,1,1]]

none = [
	[1,1,1,1,1,1,1,1],
	[1,1,1,1,1,4,1,1],
	[1,1,1,1,1,4,4,1],
	[4,4,4,4,4,4,4,4],
	[4,4,4,4,4,4,4,4],
	[1,1,1,1,1,4,4,1],
	[1,1,1,1,1,4,1,1],
	[1,1,1,1,1,1,1,1]]


def drawIcon(beginX, beginY, icon, window):
	
	indexX = 0
	indexY = 0

	for y in range(beginY, beginY + iconHeight):
		for x in range(beginX, beginX + iconWidth):

			color = icon[indexY][indexX]
			window.addch(y,x,curses.ACS_BLOCK,curses.color_pair(color) | curses.A_BOLD)

			indexX = indexX + 1

		indexX = 0
		indexY = indexY + 1

	window.refresh()

