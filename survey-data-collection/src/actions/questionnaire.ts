// src/actions/getQuestionnaireData.ts

import type { Page, QuestionnaireData } from "../types";

import { fileURLToPath } from "url";
import fs from "fs/promises";
import path from "path";
import { randomInt } from "crypto";

export async function getQuestionnaireData(): Promise<QuestionnaireData> {
  // determine root differently in dev vs prod
  let root: string;
  if (process.env.NODE_ENV !== "production") {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    root = path.join(__dirname, "../questionnaireData");
  } else {
    root = path.join(process.cwd(), "questionnaireData");
  }

  const pages: Page[] = [];

  for (const lang of ["python", "cpp", "make", "art"]) {
    const langDir = path.join(root, lang);
    let dirEntries: string[];
    try {
      dirEntries = await fs.readdir(langDir);
    } catch {
      continue; // skip if this language folder doesn't exist
    }

    for (const file of dirEntries.filter((f) => f.endsWith(".json"))) {
      const pageJsonPath = path.join(langDir, file);
      const page: Page = JSON.parse(await fs.readFile(pageJsonPath, "utf8"));

      // load introHtml if present
      if (page.introHtmlPath) {
        try {
          page.introHtml = await fs.readFile(
            path.join(root, page.introHtmlPath),
            "utf8"
          );
        } catch {
          console.warn("Intro HTML not found:", page.introHtmlPath);
        }
      }

      // for each question with a codeSnippetPath
      for (const q of page.questions) {
        if (!q.codeSnippetPath) continue;

        const snippetDir = path.join(root, q.codeSnippetPath);
        try {
          // 1) read directory entries with their types
          const dirents = await fs.readdir(snippetDir, { withFileTypes: true });
          // 2) keep only files
          const allFiles = dirents.filter((d) => d.isFile()).map((d) => d.name);
          if (allFiles.length === 0) {
            throw new Error(`No snippet files in ${snippetDir}`);
          }

          // 3) optionally filter by extension
          let candidates = allFiles;
          if (q.language) {
            const ext = "." + q.language.toLowerCase();
            const byExt = allFiles.filter((n) => n.endsWith(ext));
            if (byExt.length > 0) {
              candidates = byExt;
            }
          }

          // 4) pick one at random using crypto.randomInt for uniformity
          const idx = randomInt(0, candidates.length);
          const chosen = candidates[idx];
          const fullPath = path.join(snippetDir, chosen);

          // 5) read and assign
          q.codeSnippet = await fs.readFile(fullPath, "utf8");
          q.questionId = chosen;
        } catch (err) {
          console.error(`Error loading snippets from ${snippetDir}`, err);
          q.codeSnippet = "";
          // leave q.questionId blank if desired
        }
      }

      pages.push(page);
    }
  }

  return {
    userInfo: { name: "", yearsOfExperience: 0, email: "" },
    pages,
  };
}
