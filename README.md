# A FullStack AI-Chatbot.
-made using react,fastapi,google-adk and postgresql

## Core Features and Functionalities :-   
-the core feature of this app is the ability to manage your gmail tasks, like sending and organizing your emails using LLM(AI).  
-used Google Oauth2 for authorization for gmail access and OIDC for user authentication.(maybe could have just used Oauth2)  
-currently,it is only possible to send emails using LLM.  
-you can also chat with the your LLM.  
-The chatbot maintains session memory because the entire conversation history is persisted in a database.  

## Tech Stack  
#### 1) Frontend :- React.js, deployed on vercel   
#### 2) Backend :- Fastapi, deployed on render  
#### 3) Database :- PostgreSql, deployed on render  
#### 4) AI-Agent Framework :- ADK (Agent Development Kit) by google  

## Problem and possible fixes: 
1) The WebSocket connection currently lacks an authentication layer. This means that if a malicious user could guess or obtain a valid user_id and conversation_id, they could potentially establish a connection.
1) The client-side establishes a WebSocket connection as soon as a user switches to a conversation, and this connection remains open even if the user is idle. This isn't an efficient use of server resources, as it maintains open connections unnecessarily. This could be improved by establishing WebSocket connection only when user sends a message.
3) The google jwt id_token expires after 1 hour of login, making user login frequently. I will implement custome refresh token in future to prevent this.
4) The code is messy. Could be structured better.
