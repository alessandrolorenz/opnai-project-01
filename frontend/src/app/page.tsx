// src/pages/index.tsx
"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import AudioRecorder from "./components/AudioRecorder";
import AudioPlayer from "./components/AudioPlayer";
import { sendAudio, sendText } from "./services/apiServices";

const Home: React.FC = () => {
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioBlobRespose, setAudioBlobRespose] = useState<string | null>(null);
  const [response, setResponse] = useState<string | null>(null);
  const [transcription, setTranscription] = useState<string | null>(null);
  const [textContent, setTextContent] = useState<string | null>(null);

  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [userInput, setUserInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  
// mock
  useEffect(() => {
    const fetchTextFileMock = async () => {
      try {
        const response = await axios.get("/assets/audio.txt");
        setTextContent(response.data);
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching text file:", error);
      }
    };
    fetchTextFileMock();
  }, []);
// mock end

useEffect(() => {


}, [chatHistory]);

  const handleRecordComplete = (audioBlobProp: Blob) => {
    setAudioBlob(audioBlobProp);
  };

  const handleSendAudio = async () => {
    if (!audioBlob) return;
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    try {
      const response = await sendAudio(audioBlob);

      if(chatHistory.length > 20) {
        setChatHistory((prev) => prev.slice(1));
      }

      setChatHistory((prev) => [
        ...prev,
        { type: "user", text: transcription },
        { type: "assistant", text: response.data.resposta },
      ]);



      setTranscription(response.data.texto);
      setResponse(response.data.resposta);

      const audioUrl = response.data.audio_base64;
      const audioDataUrl = `data:audio/mpeg;base64,${audioUrl}`;

      setAudioBlobRespose(audioDataUrl);
    } catch (error) {
      console.error("Error sending audio", error);
    }
  };

  return (
    <div>
      <h1>Assistente de Áudio</h1>
      <AudioRecorder onRecordComplete={handleRecordComplete} />
      {audioBlob && <AudioPlayer audioBlob={audioBlob} />}
      <button
        className="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900"
        onClick={handleSendAudio}
        disabled={!audioBlob}
      >
        Enviar Áudio
      </button>

      {transcription && (
        <div>
          <h2>Transcrição:</h2>
          <p>{transcription}</p>
        </div>
      )}

      {response && (
        <div>
          {audioBlobRespose && <AudioPlayer audioRespose={audioBlobRespose} />}
          <h2>Resposta:</h2>
          <p>{response}</p>
        </div>
      )}

      <h2>Histórico de Conversa:</h2>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          if (userInput.trim() === "") return;

          setChatHistory((prev) => [
            ...prev,
            { type: "user", text: userInput },
          ]);

          setUserInput("");
          setIsLoading(true);
          const response = await sendText(userInput);
          setIsLoading(false);
          if (chatHistory.length > 20) {
            setChatHistory((prev) => prev.slice(1));
          }
          setChatHistory((prev) => [
            ...prev,
            { type: "assistant", text: response },
          ]);
          setResponse(response);




        }}
        className="mb-4"
      >
      <textarea
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Digite sua mensagem..."
        rows={4}
        className="w-full p-2 border border-gray-300 rounded"
      ></textarea>

      <button
        type="submit"
        className="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900"
      >
        Enviar Texto
      </button>
      </form>

      {chatHistory.map((message, index) => (
        <div key={index} className={`message ${message.type}`}>
          <strong>{message.type === "user" ? "Usuário" : "Assistente"}:</strong>
          <p>{message.text}</p>
        </div>
      ))}
    </div>
  );
};

export default Home;
