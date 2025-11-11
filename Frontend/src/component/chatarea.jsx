import { useState, useEffect, useRef } from "react";
import "./css/chatarea.css";
import axios from 'axios';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";

library.add(fas, far, fab);


function AIMessage({ chat}) {
  return <div className="ai-message"> {chat.message} </div>;
}

function UserMessage({ chat }) {
  return <div className="user-message"> {chat.message} </div>;
}

function ConversationArea({ chats }) {
  return (
    <div className="conversation-area">
      {chats.map((chat) =>
        chat.type === "ai" ? (
          <AIMessage key={chat.id} chat={chat} />
        ) : (
          <UserMessage key={chat.id} chat={chat} />
        )
      )}
    </div>
  );
}

function SubmitButton({ onClick }) {
  return (
    <button className="submit-button" onClick={onClick}>
     
      <FontAwesomeIcon icon="fa-solid fa-paper-plane" />{" "}
    </button>
  );
}

function UserInput({ input, onInput }) {
  return (
    <textarea
      className="user-input"
      value={input}
      onChange={(e) => onInput(e.target.value)}
      placeholder="how do you wanna mess with your gmail"
    ></textarea>
  );
}

function InputContainer({ input, onInput, onClick }) {
  return (
    <div className="input-container">
      <UserInput input={input} onInput={onInput} />
      <div className="input-buttons">
        <SubmitButton onClick={onClick} />{" "}
      </div>
    </div>
  );
}

export default function ChatArea({ chats, setChat ,currentConversationID, setCurrentConversationID,conversations ,setConversations}) {
  const [input, setInput] = useState("");
  
  const ws = useRef(null);

  useEffect(() => {
    if (!currentConversationID) return;
 
    const socketUrl = `ws://${process.env.REACT_APP_BACKEND_URL.replace("http://", "")}/ws/${currentConversationID}`;
      ws.current = new WebSocket(socketUrl);

         // Connection opened
    ws.current.onopen = async () => {
      console.log("WebSocket connected");
     
      ws.current.send(input);
      setInput("");

    };
    // Listen for messages
    ws.current.onmessage = (event) => {
      console.log("Received:", event.data);
      const data = JSON.parse(event.data)
      if (data.response_type === 'final'){
          setChat(prev => {
            if (prev[prev.length - 1].type === 'user'){
              return [...prev,{id:Date.now(),type:'ai',message:data.content.message}]
            }
            const updatedChats = prev.map((msg,i)=>{
            if( i === prev.length-1 && msg.type === 'ai'){
              return {...msg,message: msg.message +"\n" + data.content.message}
            }else{
              return msg;
            }});
            return updatedChats;
          });
    }
      else if(data.response_type === "tool_call"){
         setChat((prev)=>[
          ...prev,
          {id:Date.now(),type:'ai',message:'using: '+data.content.tool_name}
        ])
      }
      else if (data.response_type === 'tool_response'){
      setChat(prev => {
            const updatedChats = prev.map((msg,i)=>{
            if( i === prev.length-1){
              return {...msg,message: msg.message + "\n" + data.content.tool_response.message};
            }
            else{
              return msg;
            }
          })
            return updatedChats;
      });
       
      }
    };
    // On error
    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
    return () => {
      ws.current.close();
    };
  }, [currentConversationID]);

  // To send message manually (optional)
  const sendMessage = async () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(input);
      setChat((prev) => [...prev, { id: Date.now(), type: "user", message: input }]);
      setInput('');
    }
    else{  
        try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/users/newconversation`, {},
        {
          withCredentials: true,
        }
      );
  
      setCurrentConversationID(response.data.conversation_id);
      setConversations((prev)=>[...prev,{conversation_id:response.data.conversation_id,conversation_name:'New Conversation'}])
      
    } catch (error) {
      console.error("Error:", error);
    }
    }
    setChat((prev) => [...prev, { id: Date.now() , type: "user", message: input }]);
  };

  return (
    <div className="chat-area">
      <ConversationArea chats={chats} />
      <InputContainer input={input} onInput={setInput} onClick={sendMessage} />
    </div>
  );
}
