import requests, zipfile, os, toml, json, threading#, shutil
from sys import argv

Sversion = "1.5"

class colors(): # Class For Storing Color Codes, For AESTHETIC Purpses
	green = "\033[32m\033[1m"
	red = "\033[31m\033[1m"
	blue = "\033[34m"
	yellow = "\033[33m"
	reset = "\033[0m"

def setup(): # Setup For Execution, To Make Sure The Nessesary Folders/Files Are Present
	if not os.path.exists("./mods"): # Checks For A "mods" Folder, To Store Downloaded Mods
		os.mkdir("./mods")

	if not os.path.exists("./resourcepacks"): # Same As ^, But With Resourcepacks
		os.mkdir("./resourcepacks")

	if not os.path.exists("./shaders"): # Same As ^, But With Shaders
		os.mkdir("./shaders")

	if not os.path.exists("./manifest.json"): # Checks If The Modpack's Manifest Is In The Same Folder
		print(f"{colors.red}ERROR:{colors.reset} {colors.blue}Manifest File Not Found, Make Sure To Put The Script In The Same Folder As The Manifest{colors.reset}"); exit()

	if len(argv) >= 2:
		if len(argv) >= 3 and argv[1] == "-t":
			global maxThreadN
			try: inputS = int(argv[2])
			except: inputS = argv[2]
			if type(inputS) is str:
				if inputS == "max": maxThreadN = 30
				else: print(f"{colors.red}ERROR:{colors.reset} {colors.blue}You Must Give A MAX Thread Number, Or Use \"max\" To Use The Max (Hardcapped) Value{colors.reset}")
			else:
				if inputS > 30: print(f"{colors.yellow}\033[1mWARNING:{colors.reset} {colors.blue}Using Values Higher Than 30 Is Not Recommended{colors.reset}")
				maxThreadN = inputS
		else:
			print(f"{colors.red}ERROR:{colors.reset} {colors.blue}You Must Give A MAX Thread Number, Or Use \"max\" To Use The Max (Hardcapped) Value{colors.reset}")

def getType(mode: int, name: str):
	newPath = "mods/"
	# This Part Checks If The File Is A ZIP;
	# If It Is, It Checks If It's A shader;
	# And Sets The Appropiate Path (shader/resourcepack)

	if ".zip" in name:
		with zipfile.ZipFile.open(name, "r") as zipF:
			for entry in zipF.infolist():
				if "shader" in entry or "shaders" in entry:
					newPath = "shaders/"
					break
				else:
					newPath = "resourcepacks/"
	# Move File
	if mode == 1: print(f"\033[1A├ {colors.blue}Getting Mod Type... {colors.green}[DONE]{colors.reset}")
	os.rename(name, f"./{newPath}{name}")

def downloadM(pID, fID, listing):
	Trying2 = True

	print(f"{colors.blue}Downloading: {colors.yellow}{pID}{colors.reset} - {colors.yellow}{fID}{colors.reset} {colors.blue}({listing[0]}/{listing[1]}){colors.reset}")
	print(f"└ {colors.blue}Getting Mod...{colors.reset}")
	
	# Get Mod
	url = f"https://www.curseforge.com/api/v1/mods/{pID}/files/{fID}/download"
	while Trying2:
		try:
			response = requests.get(url)
			Trying2 = False
		except:
			tmp = 1

	# Write Mod
	if response.status_code == 200:
		print(f"\033[1A├ {colors.blue}Getting Mod... {colors.green}[DONE]{colors.reset}")
		print(f"└ {colors.blue}Writing Mod To File{colors.reset}")
		
		Nname = response.url.split("/")[-1] # Get Name
		with open(f"./{Nname}", "wb") as file:
			file.write(response.content)
		
		print(f"\033[1A├ {colors.blue}Writing Mod To File... {colors.green}[DONE]{colors.reset}")
		print(f"└ {colors.blue}Getting Mod Type...{colors.reset}")

		getType(1, Nname) # Get Mod Type/Sort In Folders

		print(f"└ {colors.blue}Downloaded: {colors.green}\"{Nname}\"{colors.reset}")
	else:
		# Handle Request Exceptions
		print(f"\033[1A└ Getting Mod... {colors.red}[ERROR]{colors.reset}")
		print(f"  └ {colors.blue}HTTP Status Code: {colors.yellow}{response.status_code}")

def downloadM2(pID, fID, listing): # Threaded Version!
	from random import randint
	global i
	Trying2 = True

	# Get Mod
	url = f"https://www.curseforge.com/api/v1/mods/{pID}/files/{fID}/download"
	while Trying2:
		try:
			response = requests.get(url)
			Trying2 = False
		except:
			print(f"{colors.red}ERROR:{colors.reset} {colors.blue}Error Getting Response; Retrying...{colors.reset}")

	# Write Mod
	if response.status_code == 200:
		Nname = response.url.split("/")[-1] # Get Name
		with open(f"./{Nname}", "wb") as file:
			file.write(response.content)

		getType(2, Nname) # Get Mod Type/Sort In Folders

		print(f"{colors.green}DONE:{colors.reset} {colors.blue}\"{Nname}\" {colors.yellow}({i}/{listing}){colors.reset}")
		i += 1 # i2 Is In The Thread Itself, So It Comes Out ""Sorted""
		if i == listing + 1: print(f"{colors.green}\nDownload Complete!{colors.reset}")
	else:
		# Handle Request Exceptions
		print(f"{colors.red}ERROR:{colors.reset} {colors.blue}There Was An Error Getting The Mod! (HTTP Status Code: {colors.blue}{response.status_code}{colors.yellow}){colors.reset}")


def main(): # Main Script Function
	global i
	global maxThreadN # Max Thread Count

	with open("manifest.json", "r") as Mfile: # Open Manifest Json
			Mdata = json.load(Mfile) # Get Data

			Mversion = Mdata["minecraft"]["version"] # Get Version
			loader = Mdata["minecraft"]["modLoaders"][0]["id"].split("-")[0] # Get Loader

			# Logging
			print(f"{colors.blue}Script Version: {colors.yellow}{Sversion}{colors.reset}")
			print(f"{colors.blue}Found Mod Loader: {colors.yellow}{loader.capitalize()}{colors.reset}")
			print(f"{colors.blue}Found MC Version: {colors.yellow}{Mversion}{colors.reset}\n")

			# Iterates Through Each Mod
			# If maxThreadN Is Something Other Than Zero, Threaded Mode Is Ran
			for entry in Mdata["files"]:
				if maxThreadN == 0: # Non Thread Ver (DEF)
					downloadM(entry["projectID"], entry["fileID"], [i, len(Mdata["files"])])
					i += 1 # Add One To i, For Listing Purposes
					print()
				else: # Threaded Version
					Trying = True

					# We Dont Wanna Loose A Mod, But Also Not Surpass The Limit, So, We Try Until Trying Is False
					while Trying:
						if threading.active_count() < maxThreadN + 1: 
							threading.Thread(target=lambda: downloadM2(entry["projectID"], entry["fileID"], len(Mdata["files"]))).start() # Start Thread
							Trying = False

# Executes Script If Run Standalone
if __name__ == "__main__":
	maxThreadN = 0 # Def thread Num
	i = 1 # For Listing
	setup() # Run Setup
	try:
		main() # Start Script
	except KeyboardInterrupt:
		print(f"{colors.blue}\033[2K\n\rAborting...{colors.reset}"); exit()
	except Exception as e:
		print(f"{colors.red}\033[2K\n\rError:{colors.reset} {colors.blue}{e}{colors.reset}")

# Made By StellarSt0rm -- 2023
