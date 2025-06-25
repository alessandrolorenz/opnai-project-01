import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const sendAudio = async (audioBlob: Blob) => {
  const formData = new FormData();
  formData.append("audio", audioBlob, "audio.wav");

  const response = await axios.post(`${API_BASE_URL}/processar-audio`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response;
};

export const sendText = async (text: string) => {
    console.log("Sending text:", text);
    const response = await axios.post(`${API_BASE_URL}/processar-texto`, { texto: text }, {
        headers: {
          "Content-Type": "application/json",
        },
      });
    return response.data;
    }

export const fetchMockTextFile = async () => {
  const response = await axios.get("/assets/audio.txt");
  return response.data;
};