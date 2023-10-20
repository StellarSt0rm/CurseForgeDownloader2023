import requests, zipfile, json, os, toml

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

def downloadM(pID, fID, Mversion, loader, listing):
	global i # Get Global i

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
		try:
			# Open TMP Mod File With zipfile 
			with zipfile.ZipFile("./mod-tmp.zip", "r") as zipF:
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

			print(f"\033[1A├ {colors.blue}Getting Mod Data... {colors.green}[DONE]{colors.reset}")
		except:
			# Handle Data Exceptions
			print(f"\033[1A├ {colors.blue}Getting Mod Data... {colors.red}[ERROR]{colors.reset}")
			print(f"│ └ {colors.blue}Reason: {colors.yellow}File Is Possibly A Resoucepack, Will Add NAME Support For Them In The Future...{colors.reset}")
			Nname = f"./resourcepacks/ResourcePack{i+1}.zip" # Set Name, As The Error Means That It Is A Resourcepack
			i += 1 # Add One To i, For Next Resourcepack
		
		# Rename TMP File
		os.rename("./mod-tmp.zip", Nname)
		print(f"└ {colors.blue}Downloaded: {colors.green}\"{Nname.replace('./mods/', '')}\"{colors.reset}")
	else:
		# Handle Request Exceptions
		print(f"\033[1A└ Getting Mod... {colors.red}[ERROR]{colors.reset}")
		print(f"  └ {colors.blue}HTTP Status Code: {colors.yellow}{response.status_code}")

def main(): # Main Script Function
	global i2
	with open("manifest.json", "r") as Mfile: # Open Manifest Json
			Mdata = json.load(Mfile) # Get Data

			Mversion = Mdata["minecraft"]["version"] # Get Version
			loader = Mdata["minecraft"]["modLoaders"][0]["id"].split("-")[0] # Get Loader

			print(f"{colors.blue}Script Version: {colors.yellow}1.2 - TESTED{colors.reset}")
			print(f"{colors.blue}Found Mod Loader: {colors.yellow}{loader}{colors.reset}")
			print(f"{colors.blue}Found MC Version: {colors.yellow}{Mversion}{colors.reset}\n")

			# Execute downloadM For Each Mod
			for entry in Mdata["files"]:
				downloadM(entry["projectID"], entry["fileID"], Mversion, loader, [i2, len(Mdata["files"])])
				i2 += 1 # Add One To i2, For Listing Purposes
				print() # Formatting
				break


if __name__ == "__main__":
	i = 0 # For Resourcepack Enumeration, Until NAME Support Is Added
	i2 = 1 # For Listing How Many Mods Are Left
	setup() # Run Setup
	try:
		main() # Start Script
	except KeyboardInterrupt:
		print(f"{colors.blue}\033[2K\n\rAborting...{colors.reset}"); exit()
	except Exception as e:
		print(f"{colors.red}\033[2K\n\rError: {colors.yellow}{e}{colors.reset}")

# Made By StellarSt0rm -- Oct/20/2023