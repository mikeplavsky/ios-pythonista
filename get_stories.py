import clipboard
import console
import sys

from jira import enum_stories

def main():
	
	board = sys.argv[1]
	console.clear()
	
	enum_stories(board)

if __name__ == '__main__':
	main()
