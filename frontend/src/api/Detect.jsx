import axios from "axios";

const API_URL = "http://localhost:8600/detect";

export const detectCraters = async (file) => {
  const formData = new FormData();
  formData.append("image", file);

  const res = await axios.post(API_URL, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};