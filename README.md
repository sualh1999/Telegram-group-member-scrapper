# 📌 Telegram Group Member Scraper  

This script was created for a special case where we needed to extract usernames from a specific Telegram group and split them among team members for private messaging.  

## 🚀 **Features:**  

✅ Fetches a list of joined groups  
✅ Scrapes active members from a selected group  
✅ Allows filtering out inactive users  
✅ Saves extracted members in JSON format  
✅ Splits user lists into multiple parts for easier distribution  
✅ Option to save splits as separate files or combined  

## 🔧 **Setup & Usage:**  

### 1️⃣ Install dependencies:  
Ensure you have Python installed, then install the required packages:  
```
pip install telethon
```

### 2️⃣ Configure API Credentials:  
Edit the script and replace:  
```
API_ID = 'Replace it with your api id' 
API_HASH = 'Replace it with your api hash'
```
Get your API credentials from [my.telegram.org](https://my.telegram.org).  

### 3️⃣ Run the Script:  

#### **Scrape Members from a Group:**  
```python
python main.py -scrape
```
This will list all the groups you’ve joined and allow you to select one for scraping.  

#### **Split Extracted Members:**  
```python
python main.py -split
```
This will divide the members into equal parts for distribution.  

#### **Save Splits as Separate Files:**  
```python
python main.py -split -to-separate-files
```

#### **Include Inactive Users:**  
By default, the script excludes users who were last seen over a month ago. To include them, use:  
```python
python main.py -scrape -add-old-users
```


