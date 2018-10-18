import clipboard
import console
import sys
import webbrowser

from jira import enum_stories

def main():
	
	board = sys.argv[1]
	console.clear()
	
	enum_stories(board)
	webbrowser.open_new('shortcuts://')

if __name__ == '__main__':
	main()
