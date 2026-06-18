import { NextFunction, Request, Response } from "express";
import { supabase } from "../config/supabase";

export const authMiddleware = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith("Bearer ")) {
      res.status(401).json({
        error: "Token no proporcionado",
      });
    }

    const token = authHeader.replace("Bearer ", "");

    const {
      data: { user },
      error,
    } = await supabase.auth.getUser(token);

    if (error || !user) {
      res.status(401).json({
        error: "Token inválido",
      });
    }

    req.user = user;

    next();
  } catch (error) {
    res.status(500).json({
      error: "Error al validar la autenticación",
    });
  }
};
