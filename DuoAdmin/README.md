# Duo Admin API Sample Scripts
This repository folder contains sample Python scripts utilizing the Cisco DUO Admin API's. It is available for use by the Cisco DevNet community through Code Exchange.
For more information on the Duo Admin API, please see the following link: https://duo.com/docs/adminapi

## Duo Requirements

1. Duo account with administrator priviledges
2. Duo Admin API enabled

## Installation

1. Ensure Python 3 is installed.
   * To download and install Python 3, please visit https://www.python.org.
2. Clone the GitHub Cisco Security API's Start Now repository, create a Python virtual environment and install Python dependencies.

```bash
git clone https://github.com/CiscoDevNet/CiscoSecurityAPIsStartNow.git

cd CiscoSecurityAPIsStartNow/DuoAdmin

python3 -m venv venv

source venv/bin/sctivate

pip install -r requirements.txt
```

## Configuration

1. Login to the Duo admin panel and create a new application.

   * From the Duo dashboard click on the **Add New...** button and select **Application**.
   * Filter for *admin api* on the **Protect an Application** page.
   * Click on the **Protect** button next to the **DUO Admin Api** application.
   * Copy the **Integration key, Secret key and API Hostname** values to a file on your computer for use in configuration section 2.  Do not share these values and keep them secure. 
   * Set the **Name** value to something unique.
   * Enable all of the application permissions.
   * Click the **Save Changes** button at the bottom of the page.

2. Open the `config.py` file in the local repository and enter the following values where specified:

* `DUO_INTEGRATION_KEY = ""`
* `DUO_SECRET_KEY = ""`
* `DUO_HOSTNAME = ""`

*(Note: additional values will also be required in many of the scripts)*

## Usage
<!--
Show users how to use the code. Be specific. Use appropriate formatting when showing code snippets or command line output. If a particular [DevNet Sandbox](https://developer.cisco.com/sandbox/) or [Learning Lab](https://developer.cisco.com/learning-labs/) can be used in to provide a network or other resources to be used with this code, call that out here.
-->

#### 1. Manage users

**Run:**

```python
python get_all_users.py
```

Inspect the JSON ouput

**Run:**

```python
python create_user.py
```

The *create_user.py* script creates a new user with username *testuser*. In the script JSON output find the *user_id* value and copy it for use in the next script.

Open the *get_user_by_userid.py* file and paste the *user_id* value into the `USER_ID = ''` variable.  **Save the file**.

**Run:**

```python
python get_user_by_userid.py
```

Inspect the JSON output.

**Run:**

```python
python get_user_by_username.py
```

Inspect the JSON output.  The *get_user_by_username.py* file already has the testuser defined in the `USERNAME = 'testuser'` variable.

#### 2. Manage phones

**Run:**

```python
python get_all_phones.py
```

Inspect the JSON ouput

The *create_phone.py* requires a valid phone number to create a new phone.  Open the file and add a phone nuber to the `NUMBER = ''` variable.  Other variables are pre-populated to create an iphone device.  **Save the file**.

**Run:**

```python
python create_phone.py
```

In the *create_phone.py* script JSON output find the *phone_id* value and copy it for use in the next script.

Open the *get_phone_by_phoneid.py* file and paste the *phone_id* value into the `PHONE_ID = ''` variable.  **Save the file**.

**Run:**

```python
python get_phone_by_phoneid.py
```

Inspect the JSON output.

Open the *get_phone_by_number.py* file and add the phone number you used to create the phone in the `NUMBER = ''` variable.  **Save the file**.

**Run:**

```python
python get_phone_by_number.py
```

Inspect the JSON output.

#### 3. Manage phone to user associations

Open the *get_user_by_userid.py* file and copy the value of the `USER_ID` variable and paste it into the `USER_ID = ''` variable in the *associate_phone_with_user.py* file.  **Save the file**.

Open the *get_phone_by_phoneid.py* file and copy the value of the `PHONE_ID` variable and paste it into the `PHONE_ID = ''` variable in the *associate_phone_with_user.py* file.  **Save the file**.

**Run:**

```python
python associate_phone_with_user.py
```

The *associate_phone_with_user.py* script creates a new phone association with user *testuser*.  Inspect the JSON output.  The output only displays the success or failure status of the association. 

Open the *get_user_by_userid.py* file and copy the value of `USER_ID = ''` value into the `USER_ID = ''` variable in the *get_phone_by_userid.py*.  **Save the file**.

**Run:**

```python
python get_phone_by_userid.py
```
Inspect the JSON Output

#### 4. Manage integrations

**Run:**

```python
python get_all_integrations.py
```

Inspect the JSON output.

The *create_integration.py* is pre-populated with the varialbles `NAME = 'Test Integration'` and 
`TYPE = 'authapi'` required to create a Duo Auth API integration.

**Run:**

```python
python create_integration.py
```

Inspect the script JSON output and copy the *integration_key* value. 

Open the *get_int_by_integration_key.py* file and paste the *integration_key* value into the `INTEGRATION_KEY = ''` variable.  **Save the file**.

**Run:**

```python
python get_int_by_integration_key.py
```

Inspect the JSON output.

#### 5. Remove users, phones, associations and integrations

**Run:**

```python
python get_int_by_integration_key.py
```

Find the *integration_key* value of the *Test Integration* in the *get_int_by_integration_key.py* JSON output and copy it.  

Open the *delete_int_by_integration_key.py* file and paste the *integration_key* value into the `INTEGRATION_KEY = ''` variable.  **Save the file**.

**Run:**

```python
python delete_int_by_integration_key.py
```

Inspect the JSON output and confirm in the Duo Admin Panel that the integration has been deleted in the **Applications** menu.

**Run:**

```python
python get_user_by_userid.py
```

Find the *user_id* value of the *testuser* in the *get_user_by_userid.py* JSON output and copy it.  

Open the *disassociate_phone_from_user.py* file and paste the *user_id* value into the `USER_ID = ''` variable.  **Save the file**.

Open the *delete_user_by_userid.py* file and paste the *user_id* value into the `USER_ID = ''` variable.  **Save the file**.

**Run:**

```python
python get_phone_by_phoneid.py
```
Find the *phone_id* value of the phone in the *get_phone_by_phoneid.py* JSON output and copy it.

Open the *disassociate_phone_from_user.py* file and paste the *phone_id* value into the `PHONE_ID = ''` variable.  **Save the file**.

Open the *delete_phone_by_phoneid.py* file and paste the *phone_id* value into the `PHONE_ID = ''` variable.  **Save the file**.

**Run:**

```python
python disassociate_phone_from_user.py
```

Inspect the JSON output and confirm in the Duo Admin Panel that the phone has been removed from *testuser* in the **2FA Devices** menu.

**Run:**

```python
python delete_phone_by_phoneid.py
```

Inspect the JSON output and confirm in the Duo Admin Panel that the phone has been deleted in the **2FA Devices** menu.

**Run:**

```python
python delete_user_by_userid.py
```

Inspect the JSON output and confirm in the Duo Admin Panel that the *testuser* has been deleted in the **Users** menu.

## Known issues

No known issues.

## Getting help

Use this project at your own risk (support not provided). *If you need technical support with Cisco Duo APIs, do one of the following:*

#### Browse the Community

Check out our [Duo Comminity](https://community.duo.com/) to pose a question or to see if any questions have already been answered by our community. We monitor these forums on a best effort basis and will periodically post answers. 

#### Open A Case

* To open a case by web: http://www.cisco.com/c/en/us/support/index.html
* To open a case by email: tac@cisco.com
* For phone support: 1-800-553-2447 (U.S.)
* For worldwide support numbers: www.cisco.com/en/US/partner/support/tsd_cisco_worldwide_contacts.html

## Licensing info

See [LICENSE](../LICENSE) for details.