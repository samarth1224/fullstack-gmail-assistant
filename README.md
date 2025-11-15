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

## WorkFlow:
1)User click on google login  
2)completes the login flow  
3)backend retrives user info from token and store it in DB   
4)sets the authentication token as cookie   
5)frontend redirects to the main homepage, if backend verfies the token.

##Problem: 
1) There is no security for websocket connection.Anyone with the user_id and conversation_id can connect with server.
   - The main cause is there doesnt seem to be a way to include Cookies while establishing the websocket connection, hence no security. I need to think of some way to make it secure.
   - The better implementation would have been to use Server Sent Events(SSE)
1) the websocket connection opens up when the user switches the conversation, remaining **ideal** until the user sends the message. A better implentation that i intend to implement
in future is to only open connection when user sends a message.
3) the google jwt id_token expires after 1 hour of login, making user login frequently. I will implement custom long lived jwt token in future to prevent this.
4) the code is messy. Could be structured better.
