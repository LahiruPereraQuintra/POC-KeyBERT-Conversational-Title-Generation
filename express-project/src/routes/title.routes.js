const express = require("express");

const { generateTitle } = require("../services/title.service");

const router = express.Router();

router.post("/generate", async (req, res) => {
  const query = req.body?.query;

  if (typeof query !== "string") {
    return res.status(400).json({ error: "query must be a string" });
  }

  try {
    const data = await generateTitle(query);
    return res.json(data);
  } catch (err) {
    if (err && err.status === 503) {
      return res.status(503).json({ error: "Title service unavailable" });
    }

    if (err && err.status && err.data !== undefined) {
      return res.status(err.status).json(err.data);
    }

    return res.status(500).json({ error: "Failed to generate title" });
  }
});

module.exports = router;

