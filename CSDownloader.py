import requests, zipfile, os, toml, json, threading
from sys import argv

class colors(): # Class For Storing Color Codes, For AESTHETIC Purpses
	green = "\033[32m\033[1m"
	red = "\033[31m\033[1m"
	blue = "\033[34m"
	yellow = "\033[33m"
	reset = "\033[0m"

def setup(): # Setup For Execution, To Make Sure The Nessesary Folders/Files Are Present
	if not os.path.exists("./mods"): # Checks For A "mods" Folder, To Store Downloaded Mods
		os.mkdir("./mods")

	if not os.path.exists("./resourcepacks"): # Same as ^, But With Resourcepacks
		os.mkdir("./resourcepacks")

	if not os.path.exists("./manifest.json"): # Checks If The Modpack's Manifest Is In The Same Folder
		print(f"{colors.red}ERROR:{colors.reset} {colors.yellow}Manifest File Not Found, Make Sure To Put The Script In The Same Folder As The Manifest{colors.reset}"); exit()

	if len(argv) >= 2:
		if len(argv) >= 3 and argv[1] == "-t":
			global maxThreadN
			try: inputS = int(argv[2])
			except: inputS = argv[2]
			if type(inputS) is str:
				if inputS == "max": maxThreadN = 30
				else: print(f"{colors.red}ERROR:{colors.reset} {colors.yellow}You Must Give A MAX Thread Number, Or Use \"max\" To Use The Max (Hardcapped) Value{colors.reset}")
			else:
				if inputS > 30: print(f"{colors.yellow}WARNING: Using Higher Values Than 30 Is Not Recommended{colors.reset}")
				maxThreadN = inputS
		else:
			print(f"{colors.red}ERROR:{colors.reset} {colors.yellow}You Must Give A MAX Thread Number, Or Use \"max\" To Use The Max (Hardcapped) Value{colors.reset}")

def getData(loader, Mversion, mode: int, Rnum: int = None):
	global i # Get Global i

	# Account For Random Int, To Not Override Files When Threaded
	if mode == 1:
		output = "./mods/mod-tmp.zip"
	elif mode == 2:
		output = f"./mods/mod-tmp-{Rnum}.zip"

	try:
		# Open TMP Mod File With zipfile
		with zipfile.ZipFile(output, "r") as zipF:
			# For Fabric
			if loader == "fabric":
				jsonD = json.loads(zipF.read("fabric.mod.json").decode("utf-8")) # Open Data Json
				name = jsonD["name"] # Set Name
				version = jsonD["version"].split("+")[0] # Set Version + Split If Mod Has MC Version In It, As We Already Add It To The File

				Nname = f"./mods/{name}-{version}-{Mversion}.jar" # Set Nname Var With The Data
			
			#For Forge
			elif loader == "forge":
				# Same As In Fabric With Everything, Except With TOML
				tomlD = toml.loads(zipF.read("META-INF/mods.toml").decode("utf-8"))["mods"][0]
				name = tomlD["displayName"]
				version = tomlD["version"].split("+")[0]
				if version == "${file.jarVersion}": version = "UnknownVersion" # Fallback

				Nname = f"./mods/{name}-{version}-{Mversion}.jar"

		if mode == 1: print(f"\033[1A├ {colors.blue}Getting Mod Data... {colors.green}[DONE]{colors.reset}")
	except:
		# Handle Data Exceptions
		if mode == 1:
			print(f"\033[1A├ {colors.blue}Getting Mod Data... {colors.red}[ERROR]{colors.reset}")
			print(f"│ └ {colors.blue}Reason: {colors.yellow}File Is Possibly A Resoucepack, Will Add NAME Support For Them In The Future...{colors.reset}")
		elif mode == 2:
			print(f"{colors.red}ERROR:{colors.reset} {colors.yellow}Error Getting Mod Data, Assuming It's A Resourcepack{colors.reset}")
		Nname = f"./resourcepacks/ResourcePack{i+1}.zip" # Set Name, As The Error Means That It Is A Resourcepack
		i += 1 # Add One To i, For Next Resourcepack
		
	# Rename TMP File
	os.rename(output, Nname)
	return Nname

def downloadM(pID, fID, Mversion, loader, listing):
	# Get Mod
	print(f"{colors.blue}Downloading: {colors.yellow}{pID}{colors.reset} - {colors.yellow}{fID}{colors.reset} ({colors.yellow}{listing[0]}{colors.reset}/{colors.yellow}{listing[1]}{colors.reset})")
	url = f"https://www.curseforge.com/api/v1/mods/{pID}/files/{fID}/download"
	print(f"└ {colors.blue}Getting Mod...{colors.reset}")
	response = requests.get(url)

	# Write Mod
	if response.status_code == 200:
		print(f"\033[1A├ {colors.blue}Getting Mod... {colors.green}[DONE]{colors.reset}")
		print(f"└ {colors.blue}Writing Mod To TMP File...{colors.reset}")
		with open("./mod-tmp.zip", "wb") as file:
			file.write(response.content)
		
		print(f"\033[1A├ {colors.blue}Writing Mod To TMP File... {colors.green}[DONE]{colors.reset}")
		print(f"└ {colors.blue}Getting Mod Data...{colors.reset}")

		# Get Mod Data (Name, Version)
		Nname = getData(loader, Mversion, 1)
		print(f"└ {colors.blue}Downloaded: {colors.green}\"{Nname.replace('./mods/', '')}\"{colors.reset}")
	else:
		# Handle Request Exceptions
		print(f"\033[1A└ Getting Mod... {colors.red}[ERROR]{colors.reset}")
		print(f"  └ {colors.blue}HTTP Status Code: {colors.yellow}{response.status_code}")

def downloadM2(pID, fID, Mversion, loader, listing): # Threaded Version!
	from random import randint
	global i2

	# Get Mod
	url = f"https://www.curseforge.com/api/v1/mods/{pID}/files/{fID}/download"
	response = requests.get(url)

	# Write Mod
	if response.status_code == 200:
		Rint = randint(10000, 99999) # Make 5 Digit Random Number, To Not Override Files
		with open(f"./mods/mod-tmp-{Rint}.zip", "wb") as file:
			file.write(response.content)

		# Get Mod Data (Name, Version)
		Nname = getData(loader, Mversion, 2, Rint)

		print(f"{colors.green}DONE:{colors.reset} {colors.yellow}\"{Nname.replace('./mods/', '')}\" {colors.blue}({i2}/{listing}){colors.reset}")
		i2 += 1 # i2 Is In The Thread Itself, So It Hopefully Comes Out ""Sorted""
	else:
		# Handle Request Exceptions
		print(f"{colors.red}ERROR:{colors.reset} {colors.blue}There Was An Error Getting The Mod! (HTTP Status Code: {colors.blue}{response.status_code}{colors.yellow}){colors.reset}")


def main(): # Main Script Function
	global i2
	global maxThreadN # Max Thread Count

	with open("manifest.json", "r") as Mfile: # Open Manifest Json
			Mdata = json.load(Mfile) # Get Data

			Mversion = Mdata["minecraft"]["version"] # Get Version
			loader = Mdata["minecraft"]["modLoaders"][0]["id"].split("-")[0] # Get Loader

			print(f"{colors.blue}Script Version: {colors.yellow}1.2 - TESTED{colors.reset}")
			print(f"{colors.blue}Found Mod Loader: {colors.yellow}{loader.capitalize()}{colors.reset}")
			print(f"{colors.blue}Found MC Version: {colors.yellow}{Mversion}{colors.reset}\n")

			# Execute downloadM For Each Mod
			for entry in Mdata["files"]:
				if maxThreadN == 0: # Non Thread Ver (DEF)
					downloadM(entry["projectID"], entry["fileID"], Mversion, loader, [i2, len(Mdata["files"])])
					i2 += 1 # Add One To i2, For Listing Purposes
					print() # Formatting
				else: # Threaded Version
					Trying = True # Set Trying To True
					while Trying: # Try To Execute While Trying Is True
						if threading.active_count() < maxThreadN: # Check That Active Thread Count Is Below maxThreadN
							threading.Thread(target=lambda: downloadM2(entry["projectID"], entry["fileID"], Mversion, loader, len(Mdata["files"]))).start() # Start Thread
							Trying = False # Set Trying To False, To Stop The While Loop

maxThreadN = 0 # Def thread Num
if __name__ == "__main__":
	i = 0 # For Resourcepack Enumeration, Until NAME Support Is Added
	i2 = 1 # For Listing How Many Mods Are Left
	setup() # Run Setup
	try:
		main() # Start Script
	except KeyboardInterrupt:
		print(f"{colors.blue}\033[2K\n\rAborting...{colors.reset}"); exit()
	except Exception as e:
		print(f"{colors.red}\033[2K\n\rError:{colors.reset} {colors.yellow}{e}{colors.reset}")

# Made By StellarSt0rm -- 2023
