import zipfile, json, os, requests, threading
from subprocess import check_output as checkOUT
from tkinter import filedialog
from math import floor
from time import sleep
import tkinter as tk

settings = {"-t": 0, "data": None, "data2": None, "-u": None, "name": None, "loader": None, "version": None, "-t2": None, "last": None}
try: DownloadsDIR = checkOUT(["xdg-user-dir", "DOWNLOAD"]).decode("utf-8").strip()
except: DownloadsDIR = None
Sversion = "1.6 - GUI (BETA)"

class tkD():
	def installB():
		summary = tk.Tk()
		summary.title("Summary")
		summary.geometry("300x115")
		summary.minsize(300, 195)

		# DATA FRAME
		dataFrame = tk.Frame(summary)

		SversionLabel = tk.Label(dataFrame, text=f"Script Version: {Sversion}")
		if settings["data"] != None:
			modpackLabel = tk.Label(dataFrame, text=f"Modpack: {settings['name']}")
			versionLabel = tk.Label(dataFrame, text=f"MC Version: {settings['version']}")
			loaderLabel = tk.Label(dataFrame, text=f"Loader: {settings['loader'].split('-')[0].capitalize()}")	
		else:
			modpackLabel = tk.Label(dataFrame, text=f"URL: {settings['-u']}")
			versionLabel = tk.Label(dataFrame, text=f"MC Version: Unknown")
			loaderLabel = tk.Label(dataFrame, text=f"Loader: Unknown")	
		
		threadsLabel = tk.Label(dataFrame, text=f"Threads: {settings['-t']}")

		tk.Label(summary, text="", font=("TkDefaultFont", 5)).pack()
		dataFrame.pack()
		SversionLabel.pack()
		tk.Label(dataFrame, text="", font=("TkDefaultFont", 4)).pack()
		modpackLabel.pack()
		versionLabel.pack()
		loaderLabel.pack()
		tk.Label(dataFrame, text="", font=("TkDefaultFont", 2)).pack()
		threadsLabel.pack()

		# CONFIRM FRAME
		confirmFrame = tk.Frame(summary)
		cancelButton = tk.Button(confirmFrame, text="Cancel", command=summary.destroy)
		confirmButton = tk.Button(confirmFrame, text="Install", command=lambda: tkD.installS(summary))

		tk.Label(summary, text="", font=("TkDefaultFont", 4)).pack()
		confirmFrame.pack()
		cancelButton.pack(side="left")
		tk.Label(confirmFrame, text=" ").pack(side='left')
		confirmButton.pack(side="left")

	def installEXIT(num, progress):
		if num == 763468:
			progress.destroy()

	def installS(summary):
		global progressLabel, progress, main2Thread

		bottomButton1.config(state="disabled")
		bottomButton2.config(state="disabled")
		summary.destroy()
		
		progress = tk.Tk()
		progress.title("Download Progress")
		progress.geometry("300x100")
		

		progressLabel = tk.Label(progress, text="Downloading... 0%", font=("TkDefaultFont", 18))
		abortButton = tk.Button(progress, text="Cancel", command=lambda: tkD.installEXIT(763468, progress), state="disabled")
		
		tk.Label(progress, text="", font=("TkDefaultFont", 5)).pack()
		progressLabel.pack()
		tk.Label(progress, text="", font=("TkDefaultFont", 4)).pack()
		abortButton.pack()
		progress.protocol("WM_DELETE_WINDOW", lambda: tkD.installEXIT(1, progress))

		downloader.setup()
		main2Thread = threading.Thread(target=downloader.main, name="DownloadManager")
		main2Thread.start()

		progress.mainloop()
		

	def validateI(P):
		return P.isdigit() or P == ""
	
	def zipDialog(label):
		path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")], title="Select Modpack", initialdir=f"{DownloadsDIR}")
		if path:
			settings['data'] = None
			Zfile = zipfile.ZipFile(path, 'r')
			if 'manifest.json' in Zfile.namelist():
				with Zfile.open('manifest.json') as manifest_file:
					try:
						manifest_data = json.load(manifest_file)
						name = manifest_data.get('name', 'N/A')
						version = manifest_data.get('version', 'N/A')
						settings["loader"] = manifest_data["minecraft"]["modLoaders"][0]["id"]
						settings["version"] = manifest_data["minecraft"]["version"]
						settings["name"] = f"{name} - {version}"
						label.config(text="ZIP File Is Valid!", fg="green")
						settings['data'] = path
					except json.JSONDecodeError:
						label.config(text="Invalid ZIP File (Invalid JSON)", fg="red")
						settings['data'] = None
			else:
				label.config(text="Invalid ZIP File (No manifest.json)", fg="red")
				settings['data'] = None
			tkD.toggle.installB()
			Zfile.close()
	
	class toggle():
		def threadsF(enableThreads, threadsField):
			if enableThreads.get() == 1:
				threadsField.config(state='normal')
				if settings["-t2"] != None: settings['-t'] = settings["-t2"]
				else: settings["-t"] = 30
			else:
				threadsField.config(state='disabled')
				settings['-t2'] = settings["-t"]
				settings["-t"] = 0

		def urlF(enableURL, urlField, modpackLabel, fileSelectButton):
			if enableURL.get() == 1:
				urlField.config(state='normal')
				modpackLabel.config(state="disabled")
				fileSelectButton.config(state="disabled")
				settings['data2'] = settings['data']
				settings['data'] = None
				if urlField.get() != "": settings["-u"] = urlField.get()
			else:
				urlField.config(state='disabled')
				settings['-u'] = None
				modpackLabel.config(state="normal")
				fileSelectButton.config(state="normal")
				settings['data'] = settings['data2']
				settings['data2'] = None
			tkD.toggle.installB()
		def installB():
			if settings["data"] != None or settings["-u"] != None:
				bottomButton2.config(state="normal")
			else:
				bottomButton2.config(state="disabled")
	class FWrite():
		def threadsFW(event):
			try: settings['-t'] = int(threadsField.get())
			except: settings['-t'] = 30
			tkD.toggle.installB()
		
		def urlFW(event):
			settings['-u'] = urlField.get()
			tkD.toggle.installB()
	
	def resetD():
		settings["data"] = None
		settings["data2"] = None
		settings["-u"] = None
		settings["name"] = None
		settings["loader"] = None
		settings["version"] = None
		settings["last"] = None

		tkD.toggle.installB()
		tkD.toggle.urlF(enableURL, urlField, modpackLabel, fileSelectButton)

		enableURL.set(0)
		modpackLabel.config(text="No ZIP Selected", fg="black")
		bottomButton1.config(state="normal")


def mainRender():
	global urlField, threadsField, bottomButton2, modpackLabel, bottomButton1, bottomButton2, enableURL, urlField, fileSelectButton

	root = tk.Tk()
	root.title("Setup Window")
	root.geometry("420x220")
	root.minsize(420, 220)

	# THREADS FRAME
	threadsFrame = tk.Frame(root)

	enableThreads = tk.IntVar()
	enableThreadsBox = tk.Checkbutton(threadsFrame, text="Threads: ", variable=enableThreads, command=lambda: tkD.toggle.threadsF(enableThreads, threadsField))
	
	threadsField = tk.Entry(threadsFrame, state='disabled', validate='key', validatecommand=(root.register(tkD.validateI), '%P'))
	threadsField.bind("<KeyRelease>", tkD.FWrite.threadsFW)
	
	tk.Label(text=" ", font=("TkDefaultFont", 5)).pack()
	threadsFrame.pack()
	enableThreadsBox.pack(side='left')
	tk.Label(threadsFrame, text=" ").pack(side='left')
	threadsField.pack(side='left')

	# URL FRAME
	urlFrame = tk.Frame(root)

	enableURL = tk.IntVar()
	enableURLBox = tk.Checkbutton(urlFrame, text="URL: ", variable=enableURL, command=lambda: tkD.toggle.urlF(enableURL, urlField, modpackLabel, fileSelectButton), state="disabled")


	urlField = tk.Entry(urlFrame, state='disabled')
	urlField.bind("<KeyRelease>", tkD.FWrite.urlFW)

	tk.Label(text="", font=("TkDefaultFont", 10)).pack()
	urlFrame.pack()
	enableURLBox.pack(side='left')
	tk.Label(urlFrame, text=" ").pack(side='left')
	urlField.pack(side='left')

	# MODPACK SELECTOR FRAME
	modpackFrame = tk.Frame(root)

	fileSelectButton = tk.Button(modpackFrame, text="Select Modpack", command=lambda: tkD.zipDialog(modpackLabel))
	modpackLabel = tk.Label(modpackFrame, text="No ZIP Selected", wraplength=350)

	tk.Label(text="", font=("TkDefaultFont", 2)).pack()
	modpackFrame.pack()
	fileSelectButton.pack(side='left')
	tk.Label(modpackFrame, text=" ").pack(side='left')
	modpackLabel.pack(side='left')

	# BUTTONS FRAME
	buttonFrame = tk.Frame(root)

	bottomButton1 = tk.Button(buttonFrame, text="Cancel", command=root.destroy)
	bottomButton2 = tk.Button(buttonFrame, text="Install", command=tkD.installB, state="disabled")

	tk.Label(text="", font=("TkDefaultFont", 30)).pack()
	buttonFrame.pack()
	bottomButton1.pack(side="left")
	tk.Label(buttonFrame, text=" ").pack(side='left')
	bottomButton2.pack(side="left")


	root.mainloop()
	

#-----------------------------------------------------------------------------

class downloader():
	def getType(mode: int, name: str, path):
		newPath = f"{path}/overrides/mods"
		# This Part Checks If The File Is A ZIP;
		# If It Is, It Checks If It's A shader;
		# And Sets The Appropiate Path (shader/resourcepack)

		if ".zip" in name:
			with zipfile.ZipFile(f"{path}/overrides/{name}", "r") as zipF:
				for entry in zipF.infolist():
					if "shader" in entry.filename or "shaders" in entry.filename:
						newPath = f"{path}/overrides/shaders"
						break
					else:
						newPath = f"{path}/overrides/resourcepacks"
		# Move File
		os.rename(f"{path}/overrides/{name}", f"{newPath}/{name}")

	def setup(): # Setup For Execution, To Make Sure The Nessesary Folders/Files Are Present
		Zpath = os.path.abspath(settings["data"].replace(settings["data"].split("/")[-1], ""))
		if not os.path.exists(f"{Zpath}/overrides"): # Chechs For Overrides Folder
			os.mkdir(f"{Zpath}/overrides")
		
		if not os.path.exists(f"{Zpath}/overrides/mods"): # Checks For A "mods" Folder, To Store Downloaded Mods
			os.mkdir(f"{Zpath}/overrides/mods")

		if not os.path.exists(f"{Zpath}/overrides/resourcepacks"): # Same As ^, But With Resourcepacks
			os.mkdir(f"{Zpath}/overrides/resourcepacks")

		if not os.path.exists(f"{Zpath}/overrides/shaders"): # Same As ^, But With Shaders
			os.mkdir(f"{Zpath}/overrides/shaders")

	class colors(): # Class For Storing Color Codes, For AESTHETIC Purpses
		green = "\033[32m\033[1m"
		red = "\033[31m\033[1m"
		blue = "\033[34m"
		yellow = "\033[33m"
		reset = "\033[0m"

	def downloadM(pID, fID, listing, mode, path):
		global i
		Trying2 = True

		# Get Mod
		url = f"https://www.curseforge.com/api/v1/mods/{pID}/files/{fID}/download"
		while Trying2:
			try:
				response = requests.get(url)
				Trying2 = False
			except:
				print(f"{downloader.colors.red}ERROR:{downloader.colors.reset} {downloader.colors.blue}Error Getting Response; Retrying...{downloader.colors.reset}")

		# Write Mod
		if response.status_code == 200:

			Nname = response.url.split("/")[-1].replace("%2B", "+") # Get Name
			with open(f"{path}/overrides/{Nname}", "wb") as file:
				file.write(response.content)

			downloader.getType(mode, Nname, path) # Get Mod Type/Sort In Folders
			
			progressLabel.config(text=f"Downloading... {floor((i/listing) * 100)}%")
			print(f"{downloader.colors.green}DONE:{downloader.colors.reset} {downloader.colors.blue}\"{Nname}\" {downloader.colors.yellow}({i}/{listing}){downloader.colors.reset}")
			i += 1
			if i == listing + 1:
				print(f"{downloader.colors.green}\nDownload Complete!{downloader.colors.reset}")
				progressLabel.config(text="Download Complete!")
				sleep(2)
				progress.destroy()
				tkD.resetD()
			
		else:
			# Handle Request Exceptions
			print(f"{downloader.colors.red}ERROR:{downloader.colors.reset} {downloader.colors.blue}There Was An Error Getting The Mod! (HTTP Status Code: {downloader.colors.blue}{response.status_code}{downloader.colors.yellow}){downloader.colors.reset}")

	def main():
		try: maxThreadN = settings["-t"]
		except: maxThreadN = 0
		global i2
		global i
		i = 1
		i2 = 1

		print(maxThreadN)

		Zpath = os.path.abspath(settings["data"].replace(settings["data"].split("/")[-1], ""))
		Zpath2 = os.path.abspath(settings["data"])

		with zipfile.ZipFile(Zpath2, "r") as Mzip:
			Mdata = json.loads(Mzip.read("manifest.json").decode("utf-8"))
			for entry in Mdata["files"]:
				if maxThreadN == 0: # Non Thread Ver (DEF)
					downloader.downloadM(entry["projectID"], entry["fileID"], len(Mdata["files"]), 1, Zpath)
				else: # Threaded Version
					Trying = True

					# We Dont Wanna Loose A Mod, But Also Not Surpass The Limit, So, We Try Until Trying Is False
					while Trying:
						if threading.active_count() < maxThreadN + 2: 
							threading.Thread(target=lambda: downloader.downloadM(entry["projectID"], entry["fileID"], len(Mdata["files"]), 2, Zpath), name=f"DownloadThread{i2}").start() # Start Thread
							Trying = False
							i2 += 1

		Mzip.close()
			

if __name__ == "__main__":
	i = 1
	i2 = 1
	mainRender()
