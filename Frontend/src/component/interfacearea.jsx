import SideBar from "./sidebar";
import ChatArea from "./chatarea";
import { useState } from "react";
export default function InterfaceArea() {
  const [chats, setChats] = useState([]);
  const [currentConversationID,setCurrentConversationID] = useState('');
  return (
    <div className="interface-area">
      <SideBar chats={chats} setChat={setChats} currentConversationID={currentConversationID} setCurrentConversationID={setCurrentConversationID}/>
      <ChatArea chats={chats} setChat={setChats} currentConversationID={currentConversationID} setCurrentConversationID={setCurrentConversationID}/>
    </div>
  );
}