from validate_email_address import validate_email
import dns.resolver
import socket
import smtplib
import re

def get_mx_records(domain):
	try:
		mx_records = dns.resolver.resolve(domain, 'MX')
		#return [str(mx.exchange)[:-1] for mx in mx_records], [str(mx.preference)[:-1] for mx in mx_records]
		return mx_records
	except dns.resolver.NoAnswer:
		return False
	except dns.resolver.NXDOMAIN:
		return False

def mx_connection(mx_record):
	try:
		# 进行连接测试
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5) # 设置超时时间为5秒
		result = sock.connect_ex((mx_record, 25))

		if result == 0:
			print("[+] MX Connection succeeded")
			return True
		else:
			print("[-] MX Connection failed!")
			return False

		sock.close()
	except socket.error:
		print("[+] MX Connection error")

def smtp_connection(email, mx_record):
	# Get local server hostname
	host = socket.gethostname()

	# SMTP lib setup (use debug level for full output)
	server = smtplib.SMTP()
	server.set_debuglevel(0)

	# SMTP Conversation
	server.connect(mx_record)
	server.helo(host)
	server.mail('me@domain.com')
	code, message = server.rcpt(email)
	server.quit()

	# Assume 250 as Success
	if code == 250:
		print('[+] SMTP server connection succeeded')
		return True
	else:
		print("[-] SMTP server connection failed")
		print("[-] " + email + " seems not to be valid")
		return False

def extract_email_domain(email):
	pattern = r'@(.*)$'
	match = re.search(pattern, email)
	if match:
		return match.group(1)
	else:
		return None

def syntax_check(email):
	if validate_email(email):
		return True
	else:
		return False

def email_check():
	email = input("[+] Input email address:")
	if validate_email(email):
		print("[+] The Email Address Syntax is correct")
		domain = extract_email_domain(email)
		mx_records = get_mx_records(domain)
		if mx_records != False:
			print(f"[+] MX records for {domain}:")
			for i in mx_records:
				print(f"[+] MX preference =  {i.preference} mail exchnager = {str(i.exchange)[:-1]}")
			mx_connection(str(mx_records[0].exchange)[:-1])
			smtp_connection(email, str(mx_records[0].exchange)[:-1])
		else:
			print("[-] Mx records not found!")
			print("[-] " + email + " seems not to be valid")

	else:
		print("[-] " + email + " seems not to be valid")


#if __name__ == '__main__':
#	email_check()
