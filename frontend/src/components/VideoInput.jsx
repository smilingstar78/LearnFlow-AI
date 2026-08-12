import { useState } from "react";


function VideoInput({
    onAddVideo,
    loading
}) {

    const [url, setUrl] = useState("");


    const handleSubmit = (event) => {

        event.preventDefault();

        if (!url.trim() || loading) {
            return;
        }

        onAddVideo(url.trim());

    };


    return (

        <div className="video-input">

            <div className="video-input-header">

                <span className="youtube-icon">
                    ▶
                </span>

                <div>

                    <h3>
                        Add a YouTube video
                    </h3>

                    <p>
                        Paste a video URL to start learning.
                    </p>

                </div>

            </div>


            <form onSubmit={handleSubmit}>

                <input
                    type="text"
                    value={url}
                    onChange={(event) =>
                        setUrl(event.target.value)
                    }
                    placeholder="https://youtube.com/watch?v=..."
                    disabled={loading}
                />

                <button
                    type="submit"
                    disabled={
                        loading ||
                        !url.trim()
                    }
                >

                    {loading
                        ? "Adding..."
                        : "Add Video"}

                </button>

            </form>

        </div>

    );
}

export default VideoInput;