import type { CorsOptions } from "cors";

export const corsConfig: CorsOptions = {
  origin: (origin, callback) => {
    const whiteList = [
      process.env.FRONTEND_URL,
    ].filter(Boolean);

    if (process.env.NODE_ENV === "development") {
      whiteList.push(
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
      );
    }

    if (!origin || whiteList.includes(origin)) {
      return callback(null, true);
    }

    return callback(new Error("CORS Error"));
  },

  credentials: true,
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  allowedHeaders: [
    "Content-Type",
    "Authorization",
    "Cache-Control",
  ],
};