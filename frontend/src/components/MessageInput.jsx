import { useState } from "react";


function MessageInput({
    onSend,
    disabled
}) {

    const [message, setMessage] = useState("");


    const handleSubmit = (event) => {

        event.preventDefault();

        if (!message.trim() || disabled) {
            return;
        }

        onSend(message.trim());

        setMessage("");
    };


    return (

        <form
            className="message-input-container"
            onSubmit={handleSubmit}
        >

            <input
                type="text"
                value={message}
                onChange={(event) =>
                    setMessage(event.target.value)
                }
                placeholder="Ask anything about your video..."
                disabled={disabled}
            />

            <button
                type="submit"
                disabled={
                    disabled ||
                    !message.trim()
                }
            >
                ➤
            </button>

        </form>

    );
}

export default MessageInput;