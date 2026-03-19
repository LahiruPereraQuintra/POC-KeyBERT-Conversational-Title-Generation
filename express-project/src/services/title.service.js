const axios = require("axios");

async function generateTitle(query) {
  try {
    const response = await axios.post(
      "http://localhost:8000/generate-title",
      { query }
    );
    return response.data;
  } catch (err) {
    if (!err.response) {
      const unavailable = new Error("Title service unavailable");
      unavailable.status = 503;
      throw unavailable;
    }

    const pythonError = new Error("Python service returned an error");
    pythonError.status = err.response.status;
    pythonError.data = err.response.data;
    throw pythonError;
  }
}

module.exports = { generateTitle };

