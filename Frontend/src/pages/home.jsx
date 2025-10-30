
import SideBar from "../component/sidebar";
import ChatArea from '../component/chatarea'
import { useState } from "react";
export default function Home() {
  const [chats, setChats] = useState([]);
  const [currentConversationID,setCurrentConversationID] = useState('');
  const [conversations, setConversations] = useState(null);
  return (
    <div className="interface-area">
      <SideBar chats={chats} setChat={setChats} currentConversationID={currentConversationID} 
      setCurrentConversationID={setCurrentConversationID}
      conversations = {conversations} setConversations={setConversations}
      />
      <ChatArea chats={chats} setChat={setChats} 
      currentConversationID={currentConversationID} setCurrentConversationID={setCurrentConversationID} 
      conversations = {conversations} setConversations={setConversations}
      />
    </div>
  );
}