import { useState } from "react";
import "./App.css";

import logo from "./assets/learnflow-logo.svg";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [query, setQuery] = useState("");

  const [messages, setMessages] = useState([]);

  const [loadingVideo, setLoadingVideo] =
    useState(false);

  const [loadingChat, setLoadingChat] =
    useState(false);

  const [videos, setVideos] = useState([]);

  const [currentVideo, setCurrentVideo] =
    useState(null);

  const [error, setError] = useState("");

  // ==========================================
  // ADD YOUTUBE VIDEO
  // ==========================================

  const addVideo = async () => {
    if (!youtubeUrl.trim()) {
      setError("Please enter a YouTube URL.");
      return;
    }

    setError("");
    setLoadingVideo(true);

    try {
      const response = await fetch(
        `${API_URL}/api/videos/`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            url: youtubeUrl.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Failed to add video."
        );
      }

      const newVideo = {
        video_id: data.video_id,
        transcript_chunks:
          data.transcript_chunks,
      };

      setVideos((previousVideos) => {
        const alreadyExists =
          previousVideos.some(
            (video) =>
              video.video_id ===
              data.video_id
          );

        if (alreadyExists) {
          return previousVideos;
        }

        return [
          ...previousVideos,
          newVideo,
        ];
      });

      setCurrentVideo(data.video_id);

      // IMPORTANT:
      // Clear the input but DON'T remove
      // the YouTube bar.

      setYoutubeUrl("");

      setMessages((previousMessages) => [
        ...previousMessages,

        {
          role: "system",

          content:
            "Video added successfully. Ask me anything about it.",
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingVideo(false);
    }
  };

  // ==========================================
  // SEND CHAT MESSAGE
  // ==========================================

  const sendMessage = async () => {
    if (!query.trim()) {
      return;
    }

    const userQuery = query.trim();

    setQuery("");
    setError("");

    setMessages((previousMessages) => [
      ...previousMessages,

      {
        role: "user",
        content: userQuery,
      },
    ]);

    setLoadingChat(true);

    try {
      const response = await fetch(
        `${API_URL}/api/chat`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            query: userQuery,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Something went wrong."
        );
      }

      setMessages((previousMessages) => [
        ...previousMessages,

        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (err) {
      setError(err.message);

      setMessages((previousMessages) => [
        ...previousMessages,

        {
          role: "assistant",

          content:
            "Sorry, something went wrong while processing your question.",
        },
      ]);
    } finally {
      setLoadingChat(false);
    }
  };

  // ==========================================
  // CHAT ENTER
  // ==========================================

  const handleChatKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      sendMessage();
    }
  };

  // ==========================================
  // YOUTUBE ENTER
  // ==========================================

  const handleUrlKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();

      addVideo();
    }
  };

  // ==========================================
  // EXAMPLE QUESTION
  // ==========================================

  const askExample = (question) => {
    setQuery(question);
  };

  return (
    <div className="app">

      {/* ======================================
          HEADER
      ====================================== */}

      <header className="header">

        <div className="brand">

          <img
            src={logo}
            alt="LearnFlow AI"
            className="brand-logo"
          />

          <div className="brand-info">

            <h1>
              LearnFlow AI
            </h1>

            <span>
              Your AI-powered learning assistant
            </span>

          </div>

        </div>

      </header>


      {/* ======================================
          YOUTUBE BAR
      ====================================== */}

      <div className="youtube-area">

        <div className="youtube-input-wrapper">

          {/* REAL YOUTUBE LOGO */}

          <div className="youtube-icon">

            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                fill="#FF0000"
                d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8Z"
              />

              <path
                fill="#fff"
                d="M9.6 15.8 15.8 12 9.6 8.2v7.6Z"
              />
            </svg>

          </div>


          <input
            type="text"

            value={youtubeUrl}

            onChange={(event) =>
              setYoutubeUrl(
                event.target.value
              )
            }

            onKeyDown={
              handleUrlKeyDown
            }

            placeholder="Paste a YouTube video URL..."

            disabled={loadingVideo}

            className="youtube-input"
          />


          <button
            className="youtube-button"

            onClick={addVideo}

            disabled={loadingVideo}
          >
            {loadingVideo
              ? "Adding..."
              : "Add Video"}
          </button>

        </div>


        {/* ERROR */}

        {error && (
          <div className="error">
            {error}
          </div>
        )}


        {/* ==================================
            ADDED VIDEOS
        ================================== */}

        {videos.length > 0 && (

          <div className="video-status">

            {videos.map((video) => (

              <div
                key={video.video_id}
                className={`video-pill ${
                  currentVideo ===
                  video.video_id
                    ? "selected"
                    : ""
                }`}
                onClick={() =>
                  setCurrentVideo(
                    video.video_id
                  )
                }
              >

                <span className="status-dot">
                  ●
                </span>

                <span>
                  {video.video_id}
                </span>

                {currentVideo ===
                  video.video_id && (
                  <span className="current-label">
                    Current
                  </span>
                )}

              </div>

            ))}

          </div>

        )}

      </div>


      {/* ======================================
          CHAT AREA
      ====================================== */}

      <main className="chat-container">

        <div className="messages">


          {/* ==================================
              WELCOME
          ================================== */}

          {messages.length === 0 && (

            <div className="welcome">

              <img
                src={logo}
                alt=""
                className="welcome-logo"
              />

              <h2>
                What can I help you learn?
              </h2>

              <p>
                Add a YouTube video above,
                then ask me anything about it.
              </p>


              <div className="suggestions">

                <button
                  onClick={() =>
                    askExample(
                      "What is this video about?"
                    )
                  }
                >
                  <span>✦</span>
                  What is this video about?
                </button>


                <button
                  onClick={() =>
                    askExample(
                      "What was at 2:02?"
                    )
                  }
                >
                  <span>◷</span>
                  What was at 2:02?
                </button>


                <button
                  onClick={() =>
                    askExample(
                      "Give me the main points."
                    )
                  }
                >
                  <span>✧</span>
                  Give me the main points.
                </button>

              </div>

            </div>

          )}


          {/* ==================================
              MESSAGES
          ================================== */}

          {messages.map(
            (message, index) => (

              <div
                key={index}
                className={`message-row ${message.role}`}
              >

                {message.role ===
                  "assistant" && (
                  <img
                    src={logo}
                    alt=""
                    className="message-logo"
                  />
                )}


                <div
                  className={`message-content ${
                    message.role
                  }`}
                >
                  {message.content}
                </div>

              </div>

            )
          )}


          {/* ==================================
              LOADING
          ================================== */}

          {loadingChat && (

            <div className="message-row assistant">

              <img
                src={logo}
                alt=""
                className="message-logo"
              />

              <div className="typing">

                <span></span>
                <span></span>
                <span></span>

              </div>

            </div>

          )}

        </div>


        {/* ======================================
            CHAT INPUT
        ====================================== */}

        <div className="chat-input-area">

          <div className="chat-input-box">

            <textarea
              value={query}

              onChange={(event) =>
                setQuery(
                  event.target.value
                )
              }

              onKeyDown={
                handleChatKeyDown
              }

              placeholder={
                currentVideo
                  ? "Ask anything about your video..."
                  : "Add a YouTube video to start learning..."
              }

              disabled={
                !currentVideo ||
                loadingChat
              }

              rows={1}
            />


            <button
              className="send-button"

              onClick={sendMessage}

              disabled={
                !query.trim() ||
                !currentVideo ||
                loadingChat
              }
            >

              <svg
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M21.5 3.5 10 15"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />

                <path
                  d="m21.5 3.5-4 17-7.5-5.5L21.5 3.5Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />

                <path
                  d="M10 15 3 10.5l18.5-7"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>

            </button>

          </div>


          <div className="input-hint">
            LearnFlow AI can make mistakes.
            Check important information.
          </div>

        </div>

      </main>

    </div>
  );
}

export default App;