import express from "express";
import userRouter from "./routes/userRouter";
import cors from "cors";
import { corsConfig } from "./config/cors";

const app = express();

app.use(express.json());
app.use(cors(corsConfig));

app.use("/api/user", userRouter);

export default app;
