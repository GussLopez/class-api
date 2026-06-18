import { Request, Response } from "express";
import { createClient } from "@supabase/supabase-js";

export class User {
  static getUser = async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const authHeader = req.headers.authorization;

      if (!id) {
        res.status(400).json({ error: "Id inválido" });
        return;
      }

      const token = authHeader.replace("Bearer ", "");

      if (!authHeader?.startsWith("Bearer ")) {
        return res.status(401).json({
          error: "No autorizado",
        });
      }

      const supabase = createClient(
        process.env.SUPABASE_URL!,
        process.env.SUPABASE_ANON_KEY!,
        {
          global: {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        },
      );

      const { data, error } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", id)
        .single();

      if (error) {
        res.status(500).json({
          error: error.message,
        });
        return;
      }

      res.status(200).json(data);
    } catch (error) {
      res.status(500).json({
        error: "Error interno del servidor",
      });
    }
  };
}
