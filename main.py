from functions import initDataB, dateparse, getPurchaseDataA, getPurchaseDataI, getPurchaseDataS
from overview import initDataO, overview, popular, itemStat
from tqdm import tqdm
import pandas as pd

print(" ---------------------------------")
print("|  E-commerce data expert system  |")
print(" ---------------------------------")

print("You need to initialize data to continue, initialize data? (y/n): ", end="")
selection = input()
if selection == 'y' or selection == 'Y':
	print("(1/2) Overview data initiating...", end=" ")
	initDataO()
	print("DONE.")
	print("(2/2) Purchase data initiating...", end=" ")
	initDataB()
	print("DONE.")
else:
	print("System shutdown...", end=" ")
	exit()

while(True):
	print('\n')
	print("----------- [functions] ----------")
	print("| 1 -- Overview ------------------|")
	print("| 2 -- Popular items -------------|")
	print("| 3 -- Get item status -----------|")
	print("| 4 -- Get purchase analytics ----|")
	print("| q -- Quit ----------------------|")
	print(" ---------------------------------")
	print("\nSelect function:", end=" ")
	selection = str(input())
	if selection == '1':
		overview()

	elif selection == '2':
		num = int(input("Get TOP ? of items: "))
		popular(num)

	elif selection == '3':
		idx = int(input("Enter item id: "))
		itemStat(idx)

	elif selection == '4':
		print('\n')
		print(" ------- [Get analytics by] ------")
		print("| 1 -- Show all ------------------|")
		print("| 2 -- by Item ID ----------------|")
		print("| 3 -- by Session ID -------------|")
		print(" ---------------------------------")
		selection = str(input("Select mode: "))
		num = int(input("Number of data to show (enter -1 to show all): "))
		if selection == '1':
			getPurchaseDataA(num)
		elif selection == '2':
			idx = int(input("Enter item id: "))
			getPurchaseDataI(idx, num)
		elif selection == '3':
			idx = int(input("Enter session id: "))
			getPurchaseDataS(idx, num)
		else:
			print("Undefined input, please try again.")
		
		
		

	elif selection == 'q':
		print("System shutdown...", end=" ")
		exit()

	else:
		print("Undefined input, please try again.")