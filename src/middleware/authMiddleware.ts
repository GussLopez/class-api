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
      return res.status(401).json({
        error: "Token no proporcionado",
      });
    }

    const token = authHeader.replace("Bearer ", "");

    const {
      data: { user },
      error,
    } = await supabase.auth.getUser(token);

    if (error || !user) {
      return res.status(401).json({
        error: "Token inválido",
      });
    }

    (req as any).user = user;

    return next();
  } catch (error) {
    return res.status(500).json({
      error: "Error al validar la autenticación",
    });
  }
};