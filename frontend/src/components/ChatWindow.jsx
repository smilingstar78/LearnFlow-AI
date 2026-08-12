import ChatMessage from "./ChatMessage";


function ChatWindow({
    messages,
    loading
}) {

    return (
        <div className="chat-window">

            {messages.length === 0 && (

                <div className="welcome">

                    <div className="welcome-icon">
                        ✦
                    </div>

                    <h1>
                        Welcome to LearnFlow AI
                    </h1>

                    <p>
                        Add a YouTube video and ask
                        anything about it.
                    </p>

                    <div className="example-prompts">

                        <span>
                            "What is this video about?"
                        </span>

                        <span>
                            "Explain this concept simply."
                        </span>

                        <span>
                            "Give me important timestamps."
                        </span>

                    </div>

                </div>

            )}


            <div className="messages">

                {messages.map(
                    (message, index) => (

                        <ChatMessage
                            key={index}
                            message={message}
                        />

                    )
                )}

                {loading && (

                    <div className="message-row ai-row">

                        <div className="message ai-message">

                            <div className="message-label">
                                LearnFlow AI
                            </div>

                            <div className="typing">

                                <span></span>
                                <span></span>
                                <span></span>

                            </div>

                        </div>

                    </div>

                )}

            </div>

        </div>
    );
}

export default ChatWindow;