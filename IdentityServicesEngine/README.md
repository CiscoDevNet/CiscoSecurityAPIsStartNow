## **Cisco Identity Services Engine**

#### Enable the ERS (Extensible RESTful Services)

Enable the ISE REST APIs
The ISE REST APIs - also known as External RESTful Services (ERS) - are disabled by default for security. You must enable it:

1. Login to your ISE PAN using the admin or other SuperAdmin user.
2. Navigate to Administration > System > Settings and select ERS Settings from the left panel.
3. Enable the ERS APIs by selecting Enable ERS for Read/Write (Do not enable CSRF unless you know how to use the tokens.)
4. Select Save to save your changes.

#### Administrator Groups for REST APIs

The following ISE Administrator Groups allow REST API access:

	ISE Admin      Group Permissions
	---------      -----------------
	SuperAdmin     Read/Write
	ERSAdmin       Read/Write
	ERSOperator    Read Only

#### Using the Included Scripts

The ERS service runs on port 9060 on your ISE Policy Administrative Node (PAN) and Policy Services Node (PSN).  You can read/write to your PAN, but you may only read from your PSNs.

You can customize each script with your username/password, hostname, and any required variables at the top of each script.  You will need the requests and JSON libraries loaded and xml.dom.minidom for scripts that use the monitoring API.
