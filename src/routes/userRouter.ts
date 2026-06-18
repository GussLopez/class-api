import { Router } from "express";
import { authMiddleware } from "../middleware/authMiddleware";
import { User } from "../controller/userController";

const router = Router();

router.get("/:id", authMiddleware, User.getUser);

export default router;
