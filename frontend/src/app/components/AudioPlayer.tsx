import React, { useEffect, useState } from "react";

interface AudioPlayerProps {
  audioBlob?: Blob
  audioRespose?: string | null
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioBlob, audioRespose }) => {
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [audioUrlResponse, setAudioUrlResponse] = useState<string | null>(null);

  useEffect(() => {
    if (audioBlob) {
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
      return () => {
        URL.revokeObjectURL(url);
      };
    }
  }, [audioBlob]);

  useEffect(() => {
    if (audioRespose) {
      // const urlResponse = URL.createObjectURL(new Blob([audioRespose], { type: "audio/mpeg" }));

      setAudioUrlResponse(audioRespose);

    }
  }, [audioRespose]);


  return (
      <audio controls>
        {audioUrl && <source src={audioUrl} type={audioBlob?.type || "audio/wav"} />}
        <source src={audioUrl ? audioUrl : ""} type="audio/wav" />
        {audioUrlResponse && <source src={audioUrlResponse} type="audio/mpeg" />}
        Seu navegador não suporta o elemento de áudio.
      </audio>

  );
};

export default AudioPlayer;
