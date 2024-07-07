
### Step 1: Make setup.sh executable:
chmod +x setup.sh

### Step 2: Install dependencies:
./setup.sh

### I have noticed a specific bug. In my mac virtual machine I cannot download chromium-browser whilst on the tryhackme machine I cannot download chromium.
I am assuming this is most likely due to operating system difference. For now I am just going to interchange 
``options.binary_location = "/usr/bin/chromium-browser"`` 
based on device I am using but will try to figure out the exact cause.