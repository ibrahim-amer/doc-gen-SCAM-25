// /app/api/questionnaire/route.ts

import { NextResponse } from "next/server";
import type { QuestionnaireData } from "@/types";

export async function GET() {
  const data: QuestionnaireData = {
    userInfo: { name: "", yearsOfExperience: 0, email: "" },
    pages: [
      {
        intro: "This section is about JavaScript fundamentals.",
        languageExperienceField: "JavaScript",
        questions: [
          {
            type: "choice",
            image: "/images/javascript-question.png",
            question:
              "Which of the following is NOT a primary data type in JavaScript?",
            choices: [
              { text: "String", value: "string" },
              { text: "Number", value: "number" },
              { text: "Boolean", value: "boolean" },
              { text: "Object", value: "object" },
              { text: "Undefined", value: "undefined" },
            ],
          },
          {
            type: "choice",
            question: "What will this Python code output?",
            choices: [
              { text: "10", value: "10" },
              { text: "15", value: "15" },
              { text: "Error", value: "error" },
              { text: "None", value: "none" },
            ],
            codeSnippet: `def calculate_sum(n):\n  total = 0\n  for i in range(n + 1):\n    total += i\n  return total\n\nresult = calculate_sum(5)\nprint(result)`,
            language: "python",
          },
        ],
      },
      {
        intro: "This section focuses on React hooks.",
        languageExperienceField: "JavaScript",
        questions: [
          {
            type: "choice",
            image: "/images/react-useeffect.png",
            question: "What is the purpose of the `useEffect` hook in React?",
            choices: [
              { text: "To manage component state", value: "state" },
              {
                text: "To perform side effects in function components",
                value: "side_effects",
              },
              { text: "To create context", value: "context" },
              {
                text: "To optimize performance",
                value: "performance",
              },
            ],
          },
          {
            type: "text",
            question:
              "Explain the concept of closures in JavaScript in your own words.",
          },
        ],
      },
      {
        intro:
          "This section evaluates your understanding of CSS documentation.",
        languageExperienceField: "CSS",
        questions: [
          {
            type: "metrics",
            question: "Evaluate this CSS header comment.",
            codeSnippet: `.container {\n  display: flex;\n  /* What property goes here? */\n}`,
            language: "css",
          },
        ],
      },
    ],
  };
  return NextResponse.json(data);
}
