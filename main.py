
import json
import sys
import os
import glob
import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, UserStatusLastMonth, UserStatusLastWeek
from telethon.errors import ChatAdminRequiredError

API_ID = 'Replace it with your api id'
API_HASH = 'Replace it with your api hash'

async def fetch_joined_groups(client):
    groups = []
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, (Channel, Chat)) and dialog.is_group:
            try:
              groups.append({
                  "title": dialog.entity.title,
                  "username": dialog.entity.username,
                  "id": dialog.entity.id
              })
            except:
                pass
    return groups

async def scrape_group_members(client, group, add_old_users):
    members = []
    try:
        async for user in client.iter_participants(group['id'], aggressive=True):
            # Check user activity status
            if not add_old_users and isinstance(user.status, (UserStatusLastMonth, UserStatusLastWeek)):
                continue

            name = ' '.join(filter(None, [user.first_name, user.last_name]))

            # Get username or phone number
            identifier = 'None'
            if user.username:
                identifier = f'@{user.username}'
            elif user.phone:
                identifier = user.phone

            members.append([name, identifier])
    
    except ChatAdminRequiredError:
        print("\nError: You need admin rights to scrape members from private groups.")
        return None
    return members

async def scrape():
    add_old_users = '-add-old-users' in sys.argv

    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        groups = await fetch_joined_groups(client)
        
        if not groups:
            print("No groups found. Join some groups first.")
            return

        print("\nGroups you've joined:")
        for idx, group in enumerate(groups, 1):
            print(f"{idx}. {group['title']} (ID: {group['id']})")

        while True:
            try:
                selection = int(input("\nEnter group number to scrape: ")) - 1
                if 0 <= selection < len(groups):
                    selected_group = groups[selection]
                    break
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a valid number.")

        print(f"\nScraping members from: {selected_group['title']}...")
        members = await scrape_group_members(client, selected_group, add_old_users)
        
        if members is None:
            return

        filename = f"{selected_group['title']}_members.json".replace(" ", "_")
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(members, f, indent=2)
        
        print(f"\nSuccessfully scraped {len(members)} members.")
        print(f"Saved to: {filename}")

def split():
    json_files = glob.glob("*.json")
    if not json_files:
        print("No JSON files found. Run with -scrape first.")
        return
    
    json_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_json = json_files[0]
    
    with open(latest_json, 'r', encoding="utf-8") as f:
        members = json.load(f)
    
    try:
        num_splits = int(input("Enter number of splits: "))
        if num_splits < 1:
            raise ValueError
    except ValueError:
        print("Invalid number. Must be at least 1.")
        return

    total = len(members)
    split_size = total // num_splits or 1

    if '-to-separate-files' in sys.argv:
        for i in range(num_splits):
            start = i * split_size
            end = start + split_size
            
            if i == num_splits - 1 or end > total:
                end = total
            
            part = members[start:end]
            filename = f"group-{i+1}.txt"
            with open(filename, 'w', encoding="utf-8") as f:
                for name, identifier in part:
                    f.write(f"{name} - {identifier}\n")
            print(f"Created {filename} with {len(part)} users")
    else:
        base_name = os.path.splitext(latest_json)[0]
        output_filename = f"{base_name}_combined.txt"
        
        with open(output_filename, 'w', encoding="utf-8") as out_file:
            for i in range(num_splits):
                start = i * split_size
                end = start + split_size
                
                if i == num_splits - 1 or end > total:
                    end = total
                
                part = members[start:end]
                out_file.write(f"{'=' * 15}\n")
                out_file.write(f"group-{i+1}:\n")
                out_file.write(f"{'-' * 15}\n")
                for name, identifier in part:
                    out_file.write(f"{name} - {identifier}\n")
                out_file.write(f"{'-' * 15}\n\n")
        
        print(f"\nCreated combined file with {num_splits} splits in {output_filename}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py [-scrape] [-split] [-to-separate-files] [-add-old-users]")
        print("Options:")
        print("-scrape\t\tScrape group members")
        print("-split\t\tSplit results into files")
        print("-to-separate-files\tCombine splits into separate files (use it with '-split')")
        print("-add-old-users\tInclude inactive users (use it with '-scrape')")
        print("\nExamples:")
        print("python main.py -scrape")
        print("python main.py -split -to-separate-files")
        sys.exit(1)

    if '-scrape' in sys.argv:
        asyncio.run(scrape())
    if '-split' in sys.argv:
        split()
