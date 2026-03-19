const express = require("express");

const titleRoutes = require("./routes/title.routes");

const app = express();
app.use(express.json());

// Mount title proxy routes.
app.use("/api/title", titleRoutes);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Express proxy listening on http://localhost:${PORT}`);
});

