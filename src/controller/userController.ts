import { Request, Response } from "express";
import { supabase } from "../config/supabase";

export class User {
  static getUser = async (req: Request, res: Response) => {
    try {

      const { id } = req.params;
      console.log(id);
      if (!id) {
        res.status(400).json({ error: "Id inválido" });
        return;
      }

      const { data, error } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", id)
        .single();

      if (error) {
        console.log(error);
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
