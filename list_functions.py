#!/usr/bin/python3
import frida, sys, getopt
packageName = ''
className = ''
def on_message(message,data):
	if message['type'] == 'send':
		print("[*] {0}".format(message['payload']))
	else:
		print(message)
def get_code_ready(className):
	code= """
	Java.perform(function()
	{
		var a = Java.use(\"""" + className + """\");
		var b = Object.getOwnPropertyNames(a.__proto__);
		console.log(b.length);
		for(i=0;i<b.length;i++)
			{
			send(b[i]);
			}
	});
	"""
	return code
def get_frida_ready(packageName,className):
	device = frida.get_usb_device()
	pid = device.spawn([packageName])
	process = device.attach(pid)
	className = packageName+'.'+className
	print(className)
	finalCode = get_code_ready(className);
	script = process.create_script(finalCode)
	script.on('message', on_message)

	script.load()
	device.resume(pid)
	sys.stdin.read()

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hp:c:",["package=","class="])
	except getopt.GetoptError:
		print("[*] Usage: python3 master.py -p <package> -c <className>")
		sys.exit(2)
	if(len(opts) != 2):
		print("[*] Usage: python3 master.py -p <package> -c <className>")
		sys.exit(2)
	for opt, arg in opts:
		if(opt == "-h"):
			print("[*] Usage: python3 master.py -c <className>")
			sys.exit()
		elif(opt == "-c"):
			className = arg
		elif(opt == "-p"):
			packageName = arg
	print("[*] Searching for the functions inside class:", className, "And Package" , packageName)

	get_frida_ready(str(packageName),str(className))


if __name__ == "__main__":
	main(sys.argv[1:])
