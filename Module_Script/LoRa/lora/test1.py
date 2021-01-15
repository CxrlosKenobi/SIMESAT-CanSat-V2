import sys
import os
import datetime
import getopt

#gateway id/addr, just for giving a different name to various log files
_gwaddr=1

def main(argv):
	try:
		opts, args = getopt.getopt(argv,'a:',['addr'])
	except getopt.GetoptError:
		print 'logParseGateway -a'
		sys.exit(2)
	
	for opt, arg in opts:		
		if opt in ("-a", "--addr"):
			global _gwaddr
			_gwaddr = arg
			print "will use _"+str(_gwaddr)+" for post-processing log file"			

		
if __name__ == "__main__":
	main(sys.argv[1:])
	

_parselog_filename = str(_gwaddr)+".log"
the_line=sys.stdin.readline()

try:
	while the_line:
		f=open(os.path.expanduser(_parselog_filename),"a")	
		now = datetime.datetime.now()
		f.write(now.isoformat()+'> ')
		f.write(the_line)
		f.close()
		sys.stdout.write(the_line)
		the_line=sys.stdin.readline()

except KeyboardInterrupt:
   sys.stdout.flush()
   pass
