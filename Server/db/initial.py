import subprocess, signal, os, time


try:
        subprocess.call(['rm', 'test.db'])
except Exception as e:
        print("Deleting database : " + str(e))

try:
	p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
	out, err = p.communicate()

	for line in out.splitlines():
		if 'python' in line:
			pid = int(line.split('  ')[1])
			print pid
			os.kill(pid, signal.SIGKILL)
except Exception as e:
	print("Killing processes : " + str(e))

'''
time.sleep(0.5)

try:
        os.call(['python', 'pythonServer.py'])
except Exception as e:
	print("Running Server : " + str(e))
'''


