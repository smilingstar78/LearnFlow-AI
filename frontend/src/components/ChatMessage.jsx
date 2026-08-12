function ChatMessage({ message }) {

    return (
        <div
            className={`message-row ${
                message.role === "user"
                    ? "user-row"
                    : "ai-row"
            }`}
        >

            <div
                className={`message ${
                    message.role === "user"
                        ? "user-message"
                        : "ai-message"
                }`}
            >

                <div className="message-label">

                    {message.role === "user"
                        ? "You"
                        : "LearnFlow AI"}

                </div>

                <div className="message-content">

                    {message.content}

                </div>

            </div>

        </div>
    );
}

export default ChatMessage;