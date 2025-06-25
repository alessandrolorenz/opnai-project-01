// src/components/AudioRecorder.tsx
import React, { useState, useRef } from "react";

interface AudioRecorderProps {
  onRecordComplete: (audioBlob: Blob) => void;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ onRecordComplete }) => {

  const mediaRecorderRef = useRef(null as MediaRecorder | null);
  const audioChunksRef = useRef([] as Blob[]);
  const mediaStreamRef = useRef( null as MediaStream | null);

  const startRecording1 = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaStreamRef.current = stream;
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];
    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.start();
  };

  const stopRecording1 = async () => {
    if (mediaRecorderRef.current) {

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
        onRecordComplete(audioBlob);
        audioChunksRef.current = [];
      };

      mediaRecorderRef.current.stop();

      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      }
    }
  };

  return (
    <div>
      <button
        className="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
        onClick={startRecording1}
        // disabled={isRecording}
      >
        Iniciar Gravação
      </button>
      <button
        className="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900"
        onClick={stopRecording1}
        // disabled={!isRecording}
      >
        Parar Gravação
      </button>
    </div>
  );
};

export default AudioRecorder;
