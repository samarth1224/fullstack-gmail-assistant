import { useEffect, useState } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";

/* import all the icons in Free Solid, { id: 2, conversation_name: "my name is samarth nomade sai adjaslda" }Free Regular, and Brands styles */
import { fas } from "@fortawesome/free-solid-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";

import "./css/sidebar.css";

library.add(fas, far, fab);

export default function SideBar({ chat, setChat, currentConversationID, setCurrentConversationID}) {
  const [sideBarOpen, setSideBarOpen] = useState(true);
  const [conversations, setConversations] = useState(null);

  const toggleSidebar = () => {
    setSideBarOpen((prev) => !prev);
  };
  useEffect(() => {
    let active = true;
    const fetchConversation = async () =>{
    try{
      const response = await axios.get(
           `http://127.0.0.1:8005/users/conversations`,
        {
          withCredentials: true,
        }
      );
      setConversations(response.data)
    }catch(error){
      console.error(error);
      setConversations(null)
    }
  }; fetchConversation();
  return () => {
      active = false;
    };
},[])
  

  const openConversation = async (id) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8005/users/messages/${id}`,
        {
          withCredentials: true,
        }
      );
        const chats = response.data.reduce((acc, currentMsg) => {
        const lastProcessedMsg = acc[acc.length - 1];
        if (lastProcessedMsg &&
            lastProcessedMsg.type === 'ai' &&
            currentMsg.message_type === 'ai') {
            lastProcessedMsg.message += "\n" + currentMsg.message_content;
        } else if (currentMsg.message_type === 'user') {
            // Push all user messages
            acc.push({
                id: currentMsg.message_id,
                type: currentMsg.message_type,
                message: currentMsg.message_content,
            });
    
        } else if (currentMsg.message_type === 'ai' &&
                   (!lastProcessedMsg || lastProcessedMsg.type === 'user')) {
            
            acc.push({
                id: currentMsg.message_id,
                type: currentMsg.message_type,
                message: currentMsg.message_content,
            });
        }
    
        return acc;
    }, []);

      setChat(chats);
      setCurrentConversationID(id);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      {sideBarOpen && (
        <div className="overlay" onClick={() => setSideBarOpen(false)} />
      )}

      <div className={`sidebar ${sideBarOpen ? "open" : ""}`}>
        <button className="sidebar-button toggle-btn" onClick={toggleSidebar}>
          <FontAwesomeIcon icon="fa-regular fa-window-maximize" />
          <span className="sidebar-text">Toggle Sidebar</span>
        </button>

        <button className="sidebar-button" onClick={() => {
                                                            setChat([]);
                                                            setCurrentConversationID(null);
                                                        }}>
          <FontAwesomeIcon icon="fa-regular fa-edit" />
          <span className="sidebar-text">New Chat</span>
        </button>

        <div className="chat-history">
          <h4 className="sidebar-text chat-history-title">Recent</h4>
          <ul className="chat-history-list">
            {conversations ? (
      conversations.map((conv) => (
        <li
          key={conv.conversation_id}
          className="sidebar-text chat-history-item"
          onClick={() => openConversation(conv.conversation_id)}
        >
          {conv.conversation_name}
        </li>
      ))
    ) : (
      <li className="sidebar-text chat-history-item empty">No conversations yet</li>
            )}
          </ul>
        </div>
      </div>
    </>
  );
}
