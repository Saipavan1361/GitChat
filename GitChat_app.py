import streamlit as st
from git import Repo
import os
import shutil
import json
from streamlit_autorefresh import st_autorefresh

CONFIG_PATH="config.json"
#Setting Auto refreshing value for the website for every 3 seconds to make smooth experience
Auto_refresh=3000

default_data = {
    "your_username": "",
    "your_token": "",
    "your_repo_url": "",
    "partners": {}
}
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        default_data = json.load(f)

st.set_page_config("GitChat💭",layout="centered")
st.title("GitHub based Messenger")

#INPUT FIELDS
st.warning("MAKE SURE THE REPO's YOU CREATED IS PRIVATE AND HAVE 'chats/'FOLDER")
your_username=st.text_input("Your GtHub Username",value=default_data["your_username"])
st.warning("Enter the username of GitHub. Do not enter the random one")
your_token=st.text_input("Your GitHub Personal Access Token",type="password",value=default_data["your_token"])
your_repo_url=st.text_input("Your GitHub repo URL",value=default_data["your_repo_url"])
st.markdown("------")
partner_username=st.text_input("Partner GitHub Username")
st.warning("Enter the username of GitHub. Do not enter the random one")
partner_token=st.text_input("Partner GitHub Personal Access Token",type="password",value=default_data["partners"].get(partner_username, {}).get("token", ""))
partner_repo_url=st.text_input("Partner GitHub repo URL",value=default_data["partners"].get(partner_username, {}).get("repo", ""))

if "seen_counts" not in st.session_state:
    st.session_state.seen_counts = {}  

if "current_partner" not in st.session_state:
    st.session_state.current_partner = ""

if "message" not in st.session_state:
    st.session_state.message = ""

#Autorefreshing
st_autorefresh(interval=Auto_refresh, key="chat_refresh")

if st.button("Save"):
    default_data["your_username"] = your_username
    default_data["your_token"] = your_token
    default_data["your_repo_url"] = your_repo_url
    if partner_username:
        default_data["partners"][partner_username] = {
            "repo": partner_repo_url,
            "token": partner_token
        }
    with open(CONFIG_PATH, "w") as f:
        json.dump(default_data, f)
    st.success("Profile saved!")

#Loading Chat files
local_path = f"./repos/{your_username}"
chat_dir= f"./repos/{your_username}/chats"
partner_list=[]

if os.path.exists(chat_dir):
            partner_list=[f.replace(".txt","")for f in os.listdir(chat_dir) if f.endswith(".txt")]

#detect unread
def get_chat_count(partner):
    path = os.path.join(chat_dir, f"{partner}.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            return len(f.readlines())
    return 0

dropdown_options = ["➕ Start New Chat"]
for partner in partner_list:
    unread = get_chat_count(partner) > st.session_state.seen_counts.get(partner, 0)
    label = f"{partner} {'🔵' if unread else ''}"
    dropdown_options.append(label)
#dropdown_list to see the existing chats and to add new chats
selected_chat=st.selectbox("💭Select a chat",["➕"]+partner_list)

if selected_chat=="➕":
    st.session_state.current_partner = partner_username.strip()
else:
    st.session_state.current_partner = selected_chat.replace(" 🔵", "").strip()
partner = st.session_state.current_partner

def load_chat_text(partner):
    path = os.path.join(chat_dir, f"{partner}.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""
chat_text = load_chat_text(partner)
st.text_area("Chat History", chat_text, height=300, disabled=True)
st.session_state.seen_counts[partner] = chat_text.count("\n")

st.session_state.message = st.text_area("Type your message", value=st.session_state.message)
#send function            
def send_to_repo(repo_url,token,sender,recipient,msg):
        safe_url=repo_url.replace("https://",f"https://{token}@")
        local_dir=f"./repo/{sender}_to_{recipient}"
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        repo=Repo.clone_from(safe_url,local_dir)
        chat_dir=os.path.join(local_dir,"chats")
        os.makedirs(chat_dir,exist_ok=True)
        chat_file=os.path.join(chat_dir,f"{recipient}.txt")
        with open(chat_file,"a") as f:
              f.write(f"{sender}:{msg}\n")
        repo.git.add(A=True)
        repo.index.commit(f"{sender}:{msg}")
        repo.remote(name="origin").push()

#send_Button
if st.button("📤 Send"):
    if your_username and your_token and your_repo_url and partner and st.session_state.message.strip():
        try:
            send_to_repo(your_repo_url, your_token, your_username, partner, st.session_state.message.strip())

            # Lookup partner token & repo from config
            partner_info = default_data["partners"].get(partner)
            if partner_info:
                send_to_repo(partner_info["repo"], partner_info["token"], your_username, partner, st.session_state.message.strip())

            st.success("Message sent!")
            st.session_state.message = ""
        except Exception as e:
            st.error(f"Failed to send message:☠️{str(e)}")
    else:
        st.warning("⚠️Fill all required fields⚠️")
        
        